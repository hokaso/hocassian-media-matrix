import sys, os

sys.path.append(os.getcwd())
import time, json, pymysql
from datetime import datetime
from multiprocessing.managers import BaseManager
from utils.snow_id import HSIS
from db.database_handler import InstantDB
import shlex, subprocess, traceback
from tenacity import retry, wait_fixed
from utils.tools import Tools
from PIL import Image
from material_process.clip.clip_analyze import ClipAnalyze

# SERVER_IP = '127.0.0.1'
SERVER_PORT = 7968


class ServerManager(BaseManager):
    pass


class ClipWorker(object):

    def __init__(self, SERVER_IP):

        with open(os.getcwd() + "/material_process/layout.json", 'r') as f0:
            _info = json.load(f0)

        current = os.getcwd().replace("/prod/matrix-python-project", "")
        self.origin_path = current + "/matrix/material/video_clip_temp/"
        self.final_path = current + "/matrix/material/video_clip/"
        self.raw_path = current + "/matrix/material/video_clip/raw/"
        self.preview_path = current + "/matrix/material/video_clip/preview/"
        self.meta_info_path = current + "/matrix/material/video_clip/meta_info/"
        self.clip_slot_path = current + "/matrix/material/video_clip/clip_slot/"
        self.tools_handle = Tools()
        ServerManager.register("get_task_queue")
        self.server_manager = ServerManager(address=(SERVER_IP, SERVER_PORT), authkey=b'0')
        self.task_queue = None
        self.db_handle = InstantDB().get_connect()
        self.az = ClipAnalyze()
        self.info = _info["threads"]
        self.threads = None

    # TODO：记得加上重试三次退出的代码，然后清除redis缓存
    @retry(wait=wait_fixed(5))
    def start(self):
        self.server_manager.connect()
        self.task_queue = self.server_manager.get_task_queue()
        print("Client Start!")
        while True:
            instruction_set = self.task_queue.get()

            # 定义渲染强度（间接控制风扇噪音），其中peak代表服务器的忙时，idle代表服务器的闲时，仅op为true时执行
            if self.info["op"]:
                if datetime.now().hour in self.info["time"]:
                    self.threads = self.info["peak"]
                else:
                    self.threads = self.info["idle"]
            else:
                self.threads = self.info["peak"]
            print("当前档位：" + self.threads)

            if instruction_set["op"] == 1:
                print("收到导入指令！")
                self.task_queue.task_done()
                try:

                    # 采集原始素材信息
                    catch_set = f'./ffprobe -of json -select_streams v -show_streams "{self.origin_path + instruction_set["file_path"]}"'
                    catch_json = subprocess.run(shlex.split(catch_set), capture_output=True, encoding='utf-8',
                                                errors='ignore')
                    origin_info = json.loads(catch_json.stdout)

                    # 为何不判断素材后缀？因为如果这不是一个视频素材，这一步就会直接报错走人
                    assert origin_info['streams'][0]['height']
                    origin_height = origin_info['streams'][0]['height']
                    origin_width = origin_info['streams'][0]['width']
                    prop = origin_width / 640

                    # 提取素材创建时间
                    if 'tags' in origin_info['streams'][0] and 'creation_time' in origin_info['streams'][0]['tags']:
                        creation_time_temp = origin_info['streams'][0]['tags']['creation_time']
                        creation_time = creation_time_temp.replace("T", " ")[0:16]
                    else:
                        creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                    # 初步确定素材类别（后期可手动调整）
                    if 'pix_fmt' in origin_info['streams'][0]:
                        origin_pix_fmt = origin_info['streams'][0]['pix_fmt']
                        if origin_pix_fmt == 'yuv422p10le':
                            material_type = "0"
                            is_copyright = "0"
                        else:
                            material_type = "1"
                            is_copyright = "1"
                    else:
                        material_type = "1"
                        is_copyright = "1"

                    # 为预览素材提供尺寸
                    preview_height_temp = round(origin_height // prop)
                    if (preview_height_temp % 2) != 0:
                        preview_height_temp += 1
                    preview_height = str(preview_height_temp)
                    preview_width = "640"

                    # 确定渲染帧率：0~45fps：30fps、46~55fps：50fps、56~65fps：60fps、66fps以上：30fps
                    if 'avg_frame_rate' in origin_info['streams'][0]:
                        pix_rate = origin_info['streams'][0]['avg_frame_rate']
                        origin_pix_rate = eval(pix_rate)
                        if 0 < origin_pix_rate <= 45 or origin_pix_rate >= 66:
                            after_rate = 30
                        elif 46 < origin_pix_rate <= 55:
                            after_rate = 50
                        elif 56 < origin_pix_rate <= 65:
                            after_rate = 60
                        else:
                            after_rate = 30
                    else:
                        after_rate = 30

                    # 生成素材新文件名
                    after_name = HSIS.main()

                    # 将原始素材信息保存至meta.json中
                    with open(self.meta_info_path + after_name + ".json", 'w') as fp:
                        json.dump(origin_info, fp)

                    # 无损处理视频帧率并绘制代理素材
                    import_set_list = [
                        "./ffmpeg -threads ",
                        self.threads,
                        " -r ",
                        str(after_rate),
                        " -i \"",
                        self.origin_path,
                        instruction_set["file_path"],
                        "\" -crf 0 ",
                        self.final_path,
                        after_name,
                        ".mp4"
                    ]
                    import_set = "".join(import_set_list)
                    os.system(import_set)

                    self.tools_handle.assert_file_exist(self.final_path + after_name + ".mp4")

                    # 确定素材色域，此处必须使用https://johnvansickle.com/ffmpeg/静态编译好的pkg，可以下载到根目录下以./的方式引用
                    if "color_primaries" in origin_info['streams'][0] and origin_info['streams'][0]['color_primaries'] == 'bt2020':
                        import_preview_set_list = [
                            "./ffmpeg -threads ",
                            self.threads, " -i ",
                            self.final_path,
                            after_name,
                            ".mp4",
                            " -vf zscale=matrixin=709:matrix=709,format=rgb24 -crf 28 -s ",
                            preview_width,
                            "x",
                            preview_height,
                            " ",
                            self.preview_path,
                            after_name,
                            ".mp4"
                        ]
                        import_preview_set = "".join(import_preview_set_list)
                    else:
                        import_preview_set_list = [
                            "./ffmpeg -threads ",
                            self.threads, " -i ",
                            self.final_path,
                            after_name, ".mp4",
                            " -crf 28 -s ",
                            preview_width,
                            "x",
                            preview_height,
                            " ",
                            self.preview_path,
                            after_name,
                            ".mp4"
                        ]
                        import_preview_set = "".join(import_preview_set_list)

                    os.system(import_preview_set)

                    self.tools_handle.assert_file_exist(self.preview_path + after_name + ".mp4")

                    # 采集处理完成的素材的信息
                    catch_set = f'./ffprobe -of json -select_streams v -show_streams "{self.final_path + after_name + ".mp4"}"'
                    catch_json = subprocess.run(
                        shlex.split(catch_set),
                        capture_output=True,
                        encoding='utf-8',
                        errors='ignore'
                    )
                    after_info = json.loads(catch_json.stdout)

                    # 提取素材时长
                    duration_temp = round(float(after_info['streams'][0]['duration']))
                    m, s = divmod(duration_temp, 60)
                    duration = "%02d:%02d" % (m, s)

                    # 提取素材尺寸
                    material_size = str(origin_width) + "*" + str(origin_height)

                    # 录入数据
                    insert_clip_sql = "INSERT INTO mat_clip(material_path, material_size, material_time, material_note, material_status, " \
                                      "material_create, material_type, is_copyright, is_show, is_merge, error_info) " \
                                      "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                      (after_name, material_size, duration, pymysql.escape_string(instruction_set["file_path"]),
                                       '1', creation_time, material_type, is_copyright, '0', '1', '')
                    self.db_handle.modify_DB(insert_clip_sql)

                    # 删除本地文件
                    os.remove(self.origin_path + instruction_set["file_path"])

                except Exception as e:
                    traceback.print_exc()
                    print(e)

            elif instruction_set["op"] == 2:

                print("收到裁切指令！")
                self.task_queue.task_done()
                try:
                    # 根据素材种类确定最终压缩率
                    if instruction_set["material_type"] == "0":
                        clip_crf = "0"
                    else:
                        clip_crf = "18"

                    print(self.final_path)

                    # 裁剪素材及其代理文件
                    crop_set_list = [
                        "./ffmpeg -threads ",
                        self.threads,
                        " -ss ",
                        str(instruction_set["start"]),
                        " -to ",
                        str(instruction_set["end"]),
                        " -i ",
                        self.final_path,
                        instruction_set["file_path"],
                        ".mp4",
                        " -crf ",
                        clip_crf,
                        " ",
                        self.raw_path,
                        instruction_set["file_path"],
                        ".mp4"
                    ]
                    crop_set = "".join(crop_set_list)
                    os.system(crop_set)

                    self.tools_handle.assert_file_exist(self.raw_path + instruction_set["file_path"] + ".mp4")

                    crop_preview_set_list = [
                        "./ffmpeg -threads ",
                        self.threads,
                        " -ss ",
                        str(instruction_set["start"]),
                        " -to ",
                        str(instruction_set["end"]),
                        " -i ",
                        self.preview_path,
                        instruction_set["file_path"],
                        ".mp4",
                        " -c copy ",
                        self.preview_path,
                        instruction_set["file_path"],
                        "_temp.mp4"
                    ]
                    crop_preview_set = "".join(crop_preview_set_list)
                    os.system(crop_preview_set)

                    self.tools_handle.assert_file_exist(self.preview_path + instruction_set["file_path"] + "_temp.mp4")

                    # 删除旧的，将新的改回原名称
                    os.remove(self.preview_path + instruction_set["file_path"] + ".mp4")
                    os.remove(self.final_path + instruction_set["file_path"] + ".mp4")
                    os.rename(self.preview_path + instruction_set["file_path"] + "_temp.mp4",
                              self.preview_path + instruction_set["file_path"] + ".mp4")

                    # 重新获取修改后的素材信息
                    catch_set = f'./ffprobe -of json -select_streams v -show_streams "{self.preview_path + instruction_set["file_path"] + ".mp4"}"'
                    catch_json = subprocess.run(shlex.split(catch_set), capture_output=True, encoding='utf-8',
                                                errors='ignore')
                    after_info = json.loads(catch_json.stdout)

                    # 提取修改后素材时长
                    duration_temp = round(float(after_info['streams'][0]['duration']))
                    m, s = divmod(duration_temp, 60)
                    duration = "%02d:%02d" % (m, s)

                    # 提取素材截图
                    clip_length = float(after_info['streams'][0]['duration'])
                    clip_slot_point = [str(clip_length * (1 / 4)), str(clip_length * (1 / 2)),
                                       str(clip_length * (3 / 4))]
                    image_url_list = []
                    for count, ikey in enumerate(clip_slot_point):
                        image_url_list.append(self.clip_slot_path + instruction_set["file_path"] + "_" + str(count))
                        slot_set_list = [
                            "./ffmpeg -ss ",
                            ikey,
                            " -i ",
                            self.raw_path,
                            instruction_set["file_path"],
                            ".mp4",
                            " -frames:v 1 -f image2 ",
                            self.clip_slot_path,
                            instruction_set["file_path"],
                            "_",
                            str(count),
                            ".jpg"
                        ]
                        slot_set = "".join(slot_set_list)
                        os.system(slot_set)

                        self.tools_handle.assert_file_exist(self.clip_slot_path + instruction_set["file_path"] + "_" + str(count) + ".jpg")

                    # 识别素材图，返回标签（调用隔壁类的方法）
                    pic_tag_set, pic_mark, pic_meta = self.az.tag_pic(image_url_list)
                    pic_tag_list = list(pic_tag_set)

                    # 选择中间的那张作为封面图
                    slot_title_set_list = [
                        "./ffmpeg -ss ",
                        str(clip_length * (1 / 2)),
                        " -i ",
                        self.raw_path,
                        instruction_set["file_path"],
                        ".mp4",
                        " -frames:v 1 -f image2 ",
                        self.clip_slot_path,
                        instruction_set["file_path"],
                        "_cover_temp",
                        ".jpg"
                    ]
                    slot_title_set = "".join(slot_title_set_list)
                    os.system(slot_title_set)

                    self.tools_handle.assert_file_exist(self.clip_slot_path + instruction_set["file_path"] + "_cover_temp.jpg")

                    # 压缩尺寸
                    target = Image.open(self.clip_slot_path + instruction_set["file_path"] + "_cover_temp" + ".jpg")
                    prop = target.width / 640

                    preview_height = round(target.height // prop)
                    preview_width = 640

                    target = target.resize((preview_width, preview_height), Image.ANTIALIAS)
                    target = target.convert('RGB')
                    target.save(self.clip_slot_path + instruction_set["file_path"] + "_cover" + ".jpg", quality=75)

                    # 更新数据
                    update_clip_sql = "UPDATE mat_clip set material_time = '%s', material_mark = %s, material_tag = '%s', " \
                                      "material_analyze_meta = '%s', material_status = '%s' where material_id = %s" % \
                                      (duration, pic_mark,
                                       pymysql.escape_string(json.dumps(pic_tag_list, ensure_ascii=False)),
                                       pymysql.escape_string(json.dumps(pic_meta, ensure_ascii=False)), "0",
                                       instruction_set["material_id"])
                    self.db_handle.modify_DB(update_clip_sql)

                    # 删除远程
                    os.remove(self.clip_slot_path + instruction_set["file_path"] + "_cover_temp" + ".jpg")

                except Exception as e:
                    traceback.print_exc()
                    print(e)
