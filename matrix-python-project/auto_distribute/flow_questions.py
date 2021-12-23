import sys, os, json, copy, pymysql, traceback, random

sys.path.append(os.getcwd())
from db.db_pool_handler import InstantDBPool
from utils.tools import Tools, DecimalEncoder
from utils.aes_cipher import AESCipher
from auto_distribute.lark import Lark
from auto_distribute.distribute_cover_generator.render_cover import RenderCover
from multiprocessing import JoinableQueue
from multiprocessing.managers import BaseManager
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request
from auto_distribute.starter_question import StarterQuestion
from gevent import pywsgi

with open("auto_distribute/config/config.json", 'r') as f0:
    info = json.load(f0)

LOCAL_MUSIC_PATH = info["LOCAL_MUSIC_PATH"]
OUTER_URL = info["OUTER_URL"]
ADJ_KEYWORDS = info["ADJ_KEYWORDS"]

db_handle = InstantDBPool().get_connect()
msg_handle = Lark()
tools_handle = Tools()
render_cover = RenderCover()

# 初始化多线程
executor = ThreadPoolExecutor(4)

# 队列通讯端口
SERVER_IP = '0.0.0.0'
SERVER_PORT = 7967

current_cover_pic_path = os.getcwd().replace("/prod/matrix-python-project", "") + "/matrix/material/video_clip/clip_slot/"


class ServerManager(BaseManager):
    pass


task_queue = JoinableQueue()
ServerManager.register("get_task_queue", callable=lambda: task_queue)
server_manager = ServerManager(address=(SERVER_IP, SERVER_PORT), authkey=b'0')
server_manager.start()


def cover_generator(instruction_set):
    try:

        # 获取音乐详细信息
        select_current_music_detail_sql = "SELECT audio_id, audio_path, audio_name, audio_author, audio_time FROM mat_audio " \
                                          "WHERE audio_path = '%s' LIMIT 1" % instruction_set["audio_path"]
        _current_music_detail = db_handle.search(select_current_music_detail_sql)
        current_music_detail = _current_music_detail[0]
        current_music_detail["audio_time"] = tools_handle.string2timestamp(current_music_detail["audio_time"])

        # 从第一个有效素材开始选，选择N个视频素材，直到N+1个视频素材大于音乐长度
        select_all_active_clips = "select material_id, material_path, material_size, material_time, material_mark, material_tag from mat_clip " \
                                  "where material_status = '%s' and is_copyright = '%s' and has_uploaded = '%s' and is_show = '%s' order by material_id" % \
                                  ("0", "0", "0", "0")
        clip_records = db_handle.search(select_all_active_clips)

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

                # 把material_time换成timestamp，方便后期计数
                current_duration = tools_handle.string2timestamp(ikey["material_time"])
                ikey["material_time"] = current_duration
                render_clips_list.append(copy.deepcopy(ikey))
                render_clips_thumbnail["pic_path"] = ikey["material_path"] + "_1.jpg"
                render_clips_thumbnail["mark"] = float(ikey["material_mark"])
                render_clips_thumbnail_list.append(copy.deepcopy(render_clips_thumbnail))
            else:
                break

            # 如果素材长度超过10s，就算它10s，反正最后渲染的时候也只展示中间的10s
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
            keywords_list.append(copy.deepcopy(keywords_time))

        # 记得断言，列表长度必须为10，否则退出；
        # TODO 这里感觉以后得加一个消息提醒，就是如果条件不满足，就提示用户检查tag，重新等待流程开始
        assert len(keywords_list) >= 10

        # 整理出词频最高的10个，其中前3个印在封面图上，前3个写在标题里，至于tag写多少，视平台而定（反正存进一个list，灵活运用）
        keywords_list.sort(key=lambda x: x["times"], reverse=True)
        _fin_keywords_list = [i["tag"] for i in keywords_list]
        fin_keywords_list = _fin_keywords_list[:10]

        # Deactivate：shuffle选中素材
        # random.shuffle(render_clips_list)

        # 根據素材打分來排序
        render_clips_list.sort(key=lambda x: float(x["material_mark"]), reverse=True)
        random.shuffle(ADJ_KEYWORDS)

        # 随机三个形容关键字
        adj_keywords = ADJ_KEYWORDS[:3]

        # 素材列表、素材时长、素材关键字存入数据库（此处不需要考虑幂等问题）
        save_sql = "update flow_distribute set mat_list = '%s', duration = '%s', keywords = '%s', adj_keywords = '%s' where id = '%s'" % \
                   (pymysql.escape_string(json.dumps(render_clips_list, cls=DecimalEncoder, ensure_ascii=False)), duration_counter,
                    pymysql.escape_string(json.dumps(fin_keywords_list, ensure_ascii=False)),
                    pymysql.escape_string(json.dumps(adj_keywords, ensure_ascii=False)), instruction_set["flow_id"])

        db_handle.modify(save_sql)

        # 从备选封面列表里抽前三分之一作为新的封面列表
        render_clips_thumbnail_list.sort(key=lambda x: x["mark"], reverse=True)
        adoption = int(len(render_clips_thumbnail_list) / 3)
        _thumbnail_list = render_clips_thumbnail_list[:adoption]
        thumbnail_list = [i["pic_path"] for i in _thumbnail_list]

        # 随机一张图片作为封面图
        index = random.randint(0, adoption-1)

        # 放入渲染器，开始生成
        current_pic_path = render_cover.main(current_cover_pic_path + thumbnail_list[index], fin_keywords_list, instruction_set["flow_id"], adj_keywords)

        # 生成完毕后，发送新卡片展示此封面，如果用户不满意，重新生成
        msg_handle.send_cover_msg(current_pic_path, instruction_set["flow_id"], thumbnail_list, fin_keywords_list)

    except Exception as e:
        traceback.print_exc()
        print(e)


def cover_generator_refresh(instruction_set):
    try:
        thumbnail_list = instruction_set["thumbnail_list"]

        # 从回传的列表中随机选一个，生成好之后用延迟更新方法更新消息卡片
        index = random.randint(0, len(thumbnail_list)-1)

        # 随机三个形容关键字
        random.shuffle(ADJ_KEYWORDS)
        adj_keywords = ADJ_KEYWORDS[:3]

        # 放入渲染器，开始生成
        current_pic_path = render_cover.main(current_cover_pic_path + thumbnail_list[index], instruction_set["keywords"], instruction_set["flow_id"], adj_keywords)

        # 生成完毕后，更新卡片展示此封面，如果用户不满意，重新生成
        msg_handle.send_cover_refresh_msg(current_pic_path, instruction_set["flow_id"], thumbnail_list, instruction_set["keywords"], instruction_set["token"], instruction_set["open_id"])

    except Exception as e:
        traceback.print_exc()
        print(e)


def random_music():
    select_music_sql = "SELECT audio_id, audio_path, audio_name, audio_author, audio_time FROM mat_audio as t1 " \
                       "WHERE t1.audio_id>=(RAND()*(SELECT MAX(audio_id) FROM mat_audio))LIMIT 1"
    rand_music = db_handle.search(select_music_sql)
    return rand_music[0]


app = Flask(__name__, static_folder='', static_url_path='')


@app.route('/', methods=['POST'])
def flow():
    flow_data = json.loads(request.data)

    # ============== 以下为事件触发相关方法 ==============

    # 给测试写一个专用卡片，当聊天端输入特定字符时，触发本来应该定时触发的卡片，然后进行测试
    if "encrypt" in flow_data:
        cipher = AESCipher(msg_handle.app_encrypt_key)
        data = json.loads(cipher.decrypt_string(flow_data["encrypt"]))

        # 校验 verification token 是否匹配，token 不匹配说明该回调并非来自开发平台
        if data["token"] != msg_handle.app_verification_token:
            print("verification token not match, token =", data["token"])
            return "illegal"

        if "type" in data:
            msg_type = data["type"]
        else:
            return "illegal"

        # 注册机器人验证
        if msg_type == "url_verification":
            rsg = {
                "challenge": data["challenge"]
            }
            return json.dumps(rsg)

        # 接下来主要处理会话事件，如果到这一步还没返回的，当做非法处理
        if "event" in data:
            event_data = data["event"]
        else:
            return "illegal"

        # type = p2p_chat_create 首次创建会话
        # type = message 对方发消息

        # if "open_id" in event_data:
        #     open_id = event_data["open_id"]
        # else:
        #     open_id = event_data["user"]["open_id"]

        print(data)

        # 首次进入bot会话，需要向当前用户介绍机器人的用法，以及提示用户先输入1开始流程
        if event_data["type"] == "p2p_chat_create":
            return "pass"
            # return msg_handle.send_create_msg()

        # 如果输入的是普通文字或图片
        elif event_data["type"] == "message":

            # 如果输入为文字，进行文字相关的操作
            if event_data["msg_type"] == "text":

                # 输入「手动分发」手动开启分发流程
                if event_data["text"] == "手动分发":
                    sq = StarterQuestion()
                    sq.run()

                if event_data["text"] == "推进渲染":
                    test_instruction_set = {'flow_id': 45}
                    task_queue.put(test_instruction_set)

        return "fail"

    # ============== 以下为bot相关方法 ==============
    print(flow_data)

    # challenge
    if "challenge" in flow_data:
        rsg = {
            "challenge": flow_data["challenge"]
        }
        return json.dumps(rsg)

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
                cur_music["audio_path"],
                flow_data["action"]["value"]["duration"]
            )

            return msg_handle.send_continue_msg()

        # 不需要分发
        else:
            destroy_sql = "update flow_distribute set status = '%s' where id = '%s'" % ("0", flow_data["action"]["value"]["flow_id"])
            db_handle.modify(destroy_sql)
            return msg_handle.send_terminate_msg()

    # 选择音乐
    elif flow_data["action"]["value"]["flow_type"] == "choose_music":

        # 选定当前
        if flow_data["action"]["value"]["choose_music"] == "1":

            # 取出music_id存入对应流程记录，并更新状态
            update_to_render_sql = "update flow_distribute set status = '%s', audio_path = '%s' where id = '%s' and status = '%s'" % \
                                   ("2", flow_data["action"]["value"]["audio_path"], flow_data["action"]["value"]["flow_id"], "1")

            try:
                db_handle.modify(update_to_render_sql)

                # 放入队列，用于执行素材收集操作（生成缩览图→通过缩览图生成封面→首尾淡入淡出渲染→合并预处理好的素材→加上音乐→分发）
                instruction_set = {
                    "flow_id": flow_data["action"]["value"]["flow_id"],
                    "audio_path": flow_data["action"]["value"]["audio_path"]
                }

                # 抛一个生成封面图的任务给子线程，等待任务执行完毕后，再发一张卡片给用户，询问用户是否满意素材
                executor.submit(cover_generator, instruction_set)

            except Exception as e:
                # 做一个幂等，由于数据库自带锁所以能够确保一致性~
                print("也许是手抽了~")
                traceback.print_exc()
                print(e)

            return msg_handle.send_continue_music_msg()

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
                cur_music["audio_path"],
                flow_data["action"]["value"]["count"],
                flow_data["action"]["value"]["duration"]
            )

    elif flow_data["action"]["value"]["flow_type"] == "choose_cover":

        # 选定当前
        if flow_data["action"]["value"]["choose_cover"] == "1":

            instruction_set = {
                "flow_id": flow_data["action"]["value"]["flow_id"]
            }

            # 修改流程状态
            update_to_render_sql = "update flow_distribute set status = '%s', cover_pic = '%s' where id = '%s' and status = '%s'" % \
                                   ("3", flow_data["action"]["value"]["cover_pic"], flow_data["action"]["value"]["flow_id"], "2")

            try:
                db_handle.modify(update_to_render_sql)
                print(instruction_set)

                # 说明一下，为啥有些任务用子进程，有些任务用队列：如果耗时比较短的（比如图片处理）可以用子进程，不会说长期占用大量运算资源；
                # 但如果是视频渲染的话，是一个长时间占用大量资源的任务，所以需要队列，逐个完成，保证系统稳定性；
                task_queue.put(instruction_set)

            except Exception as e:
                # 做一个幂等，由于数据库自带锁所以能够确保一致性~
                print("也许是手抽了~")
                traceback.print_exc()
                print(e)

            return msg_handle.send_continue_distribute_msg()

        else:

            # 抛一个生成封面图的任务给子线程，等待任务执行完毕后，更新当前卡片，询问用户是否满意素材
            instruction_set = {
                "flow_id": flow_data["action"]["value"]["flow_id"],
                "thumbnail_list": flow_data["action"]["value"]["thumbnail_list"],
                "keywords": flow_data["action"]["value"]["keywords"],
                "token": flow_data["token"],
                "open_id": flow_data["open_id"]
            }

            executor.submit(cover_generator_refresh, instruction_set)
            return msg_handle.send_cover_wait_msg()


if __name__ == '__main__':
    app.debug = True
    server = pywsgi.WSGIServer(('0.0.0.0', 13107), application=app)
    print('web server started!')
    server.serve_forever()
