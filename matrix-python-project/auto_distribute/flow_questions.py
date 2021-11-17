import sys, os, time, json, copy
sys.path.append(os.getcwd())
from db.db_pool_handler import InstantDBPool
from auto_distribute.tools import Tools
from auto_distribute.lark import Lark
from auto_distribute.distribute_cover_generator.render_cover import RenderCover
from multiprocessing import JoinableQueue
from multiprocessing.managers import BaseManager
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request

import pymysql, traceback

with open("auto_distribute/config.json", 'r') as f0:
    info = json.load(f0)

LOCAL_MUSIC_PATH = info["LOCAL_MUSIC_PATH"]
OUTER_URL = info["OUTER_URL"]

db_handle = InstantDBPool().get_connect()
msg_handle = Lark()
tools_handle = Tools()
render_cover = RenderCover()

# 初始化多线程
executor = ThreadPoolExecutor(4)

# 队列通讯端口
SERVER_IP = '0.0.0.0'
SERVER_PORT = 7967

class ServerManager(BaseManager):
    pass

task_queue = JoinableQueue()
ServerManager.register("get_task_queue", callable=lambda: task_queue)
server_manager = ServerManager(address=(SERVER_IP, SERVER_PORT), authkey=b'0')
server_manager.start()

def cover_generator(instruction_set):

    # 获取音乐详细信息
    select_current_music_detail_sql = "SELECT audio_id, audio_path, audio_name, audio_author, audio_time FROM mat_audio " \
                                      "WHERE audio_id = '%s' LIMIT 1" % instruction_set["music_id"]
    _current_music_detail = db_handle.search(select_current_music_detail_sql)
    current_music_detail = _current_music_detail[0]
    current_music_detail["audio_time"] = tools_handle.string2timestamp(current_music_detail["audio_time"])

    # 从第一个有效素材开始选，选择N个视频素材，直到N+1个视频素材大于音乐长度
    select_all_active_clips = "select material_id, material_path, material_time, material_mark, material_tag from mat_clip " \
                              "where material_status = '%s' and is_copyright = '%s' and has_uploaded = '%s' order by material_id" % \
                              ("0", "0", "0")
    clip_records = db_handle.search_DB(select_all_active_clips)

    # 设置需要渲染的视频片段的列表
    render_clips_list = []

    # 设置上述列表素材得分前三分之一的优质的缩览图列表
    render_clips_thumbnail = {
        "pic_path": "",
        "mark": 0,
    }

    render_clips_thumbnail_list = []

    # 收集上述列表对应的tag
    all_tags = []

    # 素材长度计数器
    duration_counter = 0

    for ikey in clip_records:

        if current_music_detail["audio_time"] > duration_counter:
            raw_tag_list = json.loads(ikey["material_tag"])
            all_tags = all_tags + copy.deepcopy(raw_tag_list)
            render_clips_list.append(ikey)
            render_clips_thumbnail["pic_path"] = ikey["material_path"] + "_1.jpg"
            render_clips_thumbnail["mark"] = float(ikey["material_mark"])
            render_clips_thumbnail_list.append(copy.deepcopy(render_clips_thumbnail))
        else:
            break

        current_duration = tools_handle.string2timestamp(ikey["material_time"])
        if current_duration > 10:
            current_duration = 10
        duration_counter = current_duration + duration_counter

    # 整理tags
    keywords_list = []
    keywords_time = {
        "times": 0,
        "tag": ""
    }
    keywords_set = set()
    for tag in all_tags:
        # 单个tag的长度不能超过4个字
        if len(tag) <= 4:
            keywords_set.add(tag)

    for distinct_tag in keywords_set:
        keywords_time["tag"] = distinct_tag
        keywords_time["times"] = all_tags.count(distinct_tag)
        keywords_list.append(keywords_time)

    # 记得断言，列表长度必须为10，否则退出；
    # TODO 这里感觉以后得加一个消息提醒，就是如果条件不满足，就提示用户检查tag，重新等待流程开始
    assert len(keywords_list) >= 10

    # 整理出词频最高的10个，其中前3个印在封面图上，前3个写在标题里，至于tag写多少，视平台而定（反正存进一个list，灵活运用）
    keywords_list.sort(key=lambda x: x["times"], reverse=True)
    fin_keywords_list = [ keywords_list[i]["tag"] for i in range(0,10) ]

    # shuffle选中素材
    random.shuffle(render_clips_list)

    # 素材列表、素材时长、素材关键字存入数据库（此处不需要考虑幂等问题）
    save_sql = "update flow_distribute set mat_list = '%s', duration = '%s', keywords = '%s' where id = '%s'" % \
                (pymysql.escape_string(json.dumps(render_clips_list, ensure_ascii=False)), duration_counter,
                 pymysql.escape_string(json.dumps(fin_keywords_list, ensure_ascii=False)), instruction_set["flow_id"])

    db_handle.modify(save_sql)

    # 从备选封面列表里抽前三分之一作为新的封面列表
    render_clips_thumbnail_list.sort(key=lambda x: x["mark"], reverse=True)
    adoption = int(len(render_clips_thumbnail_list) / 3)
    thumbnail_list = render_clips_thumbnail_list[:adoption]

    # 随机一张图片作为封面图
    index = random.randint(0, adoption)

    # 放入渲染器，开始生成
    render_cover.main(thumbnail_list[index], fin_keywords_list)











def random_music():

    select_music_sql = "SELECT audio_id, audio_path, audio_name, audio_author, audio_time FROM mat_audio as t1 " \
                       "WHERE t1.audio_id>=(RAND()*(SELECT MAX(audio_id) FROM mat_audio))LIMIT 1"
    rand_music = db_handle.search(select_music_sql)
    return rand_music


app = Flask(__name__, static_folder='', static_url_path='')

@app.route('/', methods=['POST'])
def flow():
    flow_data = json.loads(request.data)
    print(flow_data)

    # 是否分发
    if flow_data["action"]["value"]["flow_type"] == "is_distributed":
        # 需要分发
        if flow_data["action"]["value"]["is_distributed"] == "1":

            # 去音乐库随机选一首歌，并将其长度和素材长度做对比
            while True:

                # 如果长度不足，就再随机一首
                cur_music = random_music()
                print(cur_music)
                if tools_handle.string2timestamp(cur_music["audio_time"]) < flow_data["action"]["value"]["duration"]:
                    break

            # 消息卡片作为传递上下文的媒介，自然需要塞很多东西……
            msg_handle.send_music_msg(
                cur_music["audio_time"],
                cur_music["audio_name"] + " - " + cur_music["audio_author"],
                flow_data["action"]["value"]["flow_id"],
                OUTER_URL + cur_music["audio_path"],
                cur_music["audio_id"],
            )

            return msg_handle.send_continue_msg()

        # 不需要分发
        else:
            destory_sql = "update flow_distribute set status = '%s' where id = '%s'" % ("0", flow_data["action"]["value"]["flow_id"])
            db_handle.modify(destory_sql)
            return msg_handle.send_terminate_msg()

    # 选择音乐
    elif flow_data["action"]["value"]["flow_type"] == "choose_music":

        # 选定当前
        if flow_data["action"]["value"]["choose_music"] == "1":

            # 取出music_id存入对应流程记录，并更新状态
            update_to_render_sql = "update flow_distribute set status = '%s', audio_id = '%s' where id = '%s' and status = '%s'" % \
                                   ("2", flow_data["action"]["value"]["music_id"], flow_data["action"]["value"]["flow_id"], "1")

            try:
                db_handle.modify(update_to_render_sql)

                # 放入队列，用于执行素材收集操作（生成缩览图→通过缩览图生成封面→首尾淡入淡出渲染→合并预处理好的素材→加上音乐→分发）
                instruction_set = {
                    "flow_id": flow_data["action"]["value"]["flow_id"],
                    "music_id": flow_data["action"]["value"]["music_id"]
                }
                # task_queue.put(instruction_set)

                # 抛一个生成封面图的任务给子线程，等待任务执行完毕后，再发一张卡片给用户，询问用户是否满意素材
                executor.submit(cover_generator, instruction_set)

            except Exception as e:
                # 做一个幂等，由于数据库自带锁所以能够确保一致性~
                print("也许是手抽了~")
                traceback.print_exc()
                print(e)

            return msg_handle.send_music_continue_msg()

        else:

            # 去音乐库随机选一首歌，并将其长度和素材长度做对比
            while True:

                # 如果长度不足，就再随机一首
                cur_music = random_music()
                print(cur_music)
                if tools_handle.string2timestamp(cur_music["audio_time"]) < flow_data["action"]["value"]["duration"]:
                    break

            # 消息卡片作为传递上下文的媒介，自然需要塞很多东西……
            return msg_handle.send_music_refresh_msg(
                cur_music["audio_time"],
                cur_music["audio_name"] + " - " + cur_music["audio_author"],
                flow_data["action"]["value"]["flow_id"],
                OUTER_URL + cur_music["audio_path"],
                cur_music["audio_id"],
                flow_data["action"]["value"]["count"]
            )


if __name__ == '__main__':
    app.debug = True
    server = pywsgi.WSGIServer(('0.0.0.0', 13107), application=app)
    print('web server started!')
    server.serve_forever()
