import sys, os, json, shutil, math, traceback, shlex, subprocess, ffmpeg

sys.path.append(os.getcwd())
from multiprocessing.managers import BaseManager
from db.db_pool_handler import InstantDBPool
from tenacity import retry, wait_fixed
from utils.tools import Tools
from auto_distribute.upload import Upload
from utils.snow_id import HSIS

# SERVER_IP = '127.0.0.1'
SERVER_PORT = 7967


class ServerManager(BaseManager):
    pass


class Render(object):

    def __init__(self, SERVER_IP):

        current = os.getcwd().replace("/prod/matrix-python-project", "")
        self.ffmpeg_path = current + "/prod/matrix-python-project/ffmpeg"
        self.raw_path = current + "/matrix/material/video_clip/raw/"
        self.music_path = current + "/matrix/material/audio_music/"
        self.current_path = "auto_distribute/"
        self.clip_bg_4k = self.current_path + "clip_bg_4k.png"
        self.tools_handle = Tools()
        self.db_handle = InstantDBPool().get_connect()
        ServerManager.register("get_task_queue")
        self.server_manager = ServerManager(address=(SERVER_IP, SERVER_PORT), authkey=b'0')
        self.task_queue = None
        self.upload = Upload()
        self.store_path = current + "/matrix/distribute/"
        self.standard_4k_w = 3840
        self.standard_4k_h = 2160

    '''
    输入：
    fw和fh代表素材原本的宽高
    
    输出：
    tw和th代表素材经过算法处理后的宽高
    lw和lh代表素材经过算法处理后左上角应该渲染在画面中的坐标（毕竟渲染器是从上至下，从左到右来渲染，所以需要左上角坐标）
    '''

    def crop_to_suit_4k(self, fw, fh):

        FOUR_KILO_W = self.standard_4k_w
        FOUR_KILO_H = self.standard_4k_h

        # 毕竟大多数都是4k素材，hardcore一下提高效率
        if fw == FOUR_KILO_W and fh == FOUR_KILO_H:
            return FOUR_KILO_W, FOUR_KILO_H, 0, 0

        if fw >= fh * 16 / 9:
            tw = FOUR_KILO_W
            th = math.ceil(FOUR_KILO_W * fh / fw)
        else:
            th = FOUR_KILO_H
            tw = math.ceil(FOUR_KILO_H * fw / fh)

        lw = int((FOUR_KILO_W - tw) / 2)
        lh = int((FOUR_KILO_H - th) / 2)

        return tw, th, lw, lh

    # @retry(wait=wait_fixed(5))
    def start(self):
        self.server_manager.connect()
        self.task_queue = self.server_manager.get_task_queue()
        print("Client Start!")
        while True:

            try:
                instruction_set = self.task_queue.get()
                if instruction_set is None:
                    continue
            except Exception as e:
                traceback.print_exc()
                print(e)
                break

            # 查库，将所有素材记录取出，如果时间长度大于1秒，说明可以淡入淡出，如果可以就处理，不行就算了。
            select_current_flow_detail_sql = "SELECT status, mat_list, audio_path, cover_pic, keywords, adj_keywords FROM flow_distribute " \
                                             "WHERE id = '%s' LIMIT 1" % instruction_set["flow_id"]
            _current_flow_detail = self.db_handle.search(select_current_flow_detail_sql)
            current_flow_detail = _current_flow_detail[0]

            # 到这里的前提条件，status一定为3
            assert current_flow_detail["status"] == "3"

            mat_list = json.loads(current_flow_detail["mat_list"])

            # 先把每一条素材处理成合适concat的temp素材片段，放置的临时文件夹名称示例：1_clip_temp
            current_clip_path = self.current_path + str(instruction_set["flow_id"]) + "_clip_temp/"
            if not os.path.exists(current_clip_path):
                os.makedirs(current_clip_path)

            # 设置concat文件
            if os.path.isfile(current_clip_path + "list.txt"):
                os.remove(current_clip_path + "list.txt")

            temp_txt_file = open(current_clip_path + "list.txt", "w+")
            mat_clip_list = []

            for ikey in mat_list:
                # 拼凑路径出来，然后处理，output到上述文件夹
                temp_origin_clip_path = self.raw_path + ikey["material_path"] + ".mp4"
                temp_clip_path = current_clip_path + ikey["material_path"] + ".mp4"

                # 这个方法可能有点问题，所以保险起见重新ffprobe
                # temp_clip_size[0] 宽
                # temp_clip_size[1] 高
                # temp_clip_size = ikey["material_size"].split("*")
                # tw, th, lw, lh = self.crop_to_suit_4k(int(temp_clip_size[0]), int(temp_clip_size[1]))

                # =============================================================

                # 采集原始素材信息
                catch_set = f'./ffprobe -of json -select_streams v -show_streams "{temp_origin_clip_path}"'
                catch_json = subprocess.run(shlex.split(catch_set), capture_output=True, encoding='utf-8',
                                            errors='ignore')
                origin_info = json.loads(catch_json.stdout)

                # 为何不判断素材后缀？因为如果这不是一个视频素材，这一步就会直接报错走人
                assert origin_info['streams'][0]['height']
                origin_height = origin_info['streams'][0]['height']
                origin_width = origin_info['streams'][0]['width']

                tw, th, lw, lh = self.crop_to_suit_4k(int(origin_width), int(origin_height))

                # =============================================================

                # 考虑素材时长问题，超过10s的截取中间10s
                temp_material_time = ikey["material_time"]
                if temp_material_time > 10:
                    start_time = temp_material_time / 2 - 5
                    end_time = temp_material_time / 2 + 5
                else:
                    start_time = 0
                    end_time = temp_material_time

                # 准备好concat的list.txt
                temp_clip_concat_record = "file " + ikey["material_path"] + ".mp4\n"
                temp_txt_file.writelines(temp_clip_concat_record)

                # 准备好concat-filter的列表
                mat_clip_list.append(ffmpeg.input(temp_clip_path))

                # 为何不用with open：效率太低，每进一个循环就需要开一次，所以还是在循环外开启，然后结束循环，待所有记录写入完毕后，再关闭文件
                # with open(current_clip_path + "list.txt", "w+") as temp_txt_file:
                #     temp_txt_file.writelines(temp_clip_concat_record)

                temp_clip_set_list = [
                    "./ffmpeg",
                    " -ss ",
                    str(start_time),
                    " -to ",
                    str(end_time),
                    " -i \"",
                    temp_origin_clip_path,
                    "\" -i \"",
                    self.clip_bg_4k,
                    "\" ",
                    # "-vf zscale=matrixin=709:matrix=709,format=yuv420p ",
                    "-filter_complex \"[0:v]scale=",
                    str(tw),
                    ":",
                    str(th),
                    "[video1];[1:v][video1]overlay=",
                    str(lw),
                    ":",
                    str(lh),
                    "\" -crf 20 -s ",
                    str(self.standard_4k_w),
                    "x",
                    str(self.standard_4k_h),
                    " -an ",
                    "-r 60 ",
                    "-video_track_timescale 60k \"",
                    current_clip_path,
                    ikey["material_path"],
                    ".mp4\""
                ]

                temp_clip_set = "".join(temp_clip_set_list)
                print(temp_clip_set)
                os.system(temp_clip_set)

                self.tools_handle.assert_file_exist(temp_clip_path)

            temp_txt_file.close()

            # 给第一条创建淡入效果，不符合持续时间两秒以上条件就跳过
            temp_first_clip_path = mat_list[0]["material_path"]
            temp_first_clip_time = mat_list[0]["material_time"]
            if temp_first_clip_time >= 2:
                temp_first_fade_in_set_list = [
                    "./ffmpeg ",
                    "-i \"",
                    current_clip_path,
                    temp_first_clip_path,
                    ".mp4\" ",
                    "-vf fade=in:0:60 -crf 20 \"",
                    current_clip_path,
                    temp_first_clip_path,
                    "_first.mp4\""
                ]

                temp_first_fade_in_set = "".join(temp_first_fade_in_set_list)
                print(temp_first_fade_in_set)
                os.system(temp_first_fade_in_set)

                self.tools_handle.assert_file_exist(current_clip_path + temp_first_clip_path + "_first.mp4")

                # 删除原来的，把新的名称改回去，当做无事发生（
                os.remove(
                    current_clip_path + temp_first_clip_path + ".mp4"
                )

                os.rename(
                    current_clip_path + temp_first_clip_path + "_first.mp4",
                    current_clip_path + temp_first_clip_path + ".mp4"
                )

            # 给最后一条创建淡出效果，不符合持续时间两秒以上条件就跳过
            temp_last_clip_path = mat_list[-1]["material_path"]
            temp_last_clip_time = mat_list[-1]["material_time"]
            if temp_last_clip_time >= 2:

                if temp_last_clip_time > 10:
                    end_time = 10
                else:
                    end_time = temp_last_clip_time

                temp_last_fade_in_set_list = [
                    "./ffmpeg ",
                    "-i \"",
                    current_clip_path,
                    temp_last_clip_path,
                    ".mp4\" ",
                    "-vf fade=out:st=",
                    str(end_time - 1),
                    ":d=1 -crf 20 \"",
                    current_clip_path,
                    temp_last_clip_path,
                    "_last.mp4\""
                ]

                temp_last_fade_in_set = "".join(temp_last_fade_in_set_list)
                print(temp_last_fade_in_set)
                os.system(temp_last_fade_in_set)

                self.tools_handle.assert_file_exist(current_clip_path + temp_last_clip_path + "_last.mp4")

                # 删除原来的，把新的名称改回去，当做无事发生（
                os.remove(
                    current_clip_path + temp_last_clip_path + ".mp4"
                )

                os.rename(
                    current_clip_path + temp_last_clip_path + "_last.mp4",
                    current_clip_path + temp_last_clip_path + ".mp4"
                )

            # 警告⚠️：ffmpeg的concat方法有问题，无法正确处理4k素材！
            # 多条合成一条，素材名称示例：1_clip_no_audio.mp4
            # concat_set_list = [
            #     "./ffmpeg -f concat -i \"",
            #     current_clip_path,
            #     "list.txt\"",
            #     " \"",
            #     self.current_path,
            #     str(instruction_set["flow_id"]),
            #     "_clip_no_audio.mp4\""
            # ]
            #
            # concat_set = "".join(concat_set_list)
            # print(concat_set)
            # os.system(concat_set)
            #
            # self.tools_handle.assert_file_exist(self.current_path + str(instruction_set["flow_id"]) + "_clip_no_audio.mp4")

            # 替代方法：使用python-ffmpeg的便捷方式来Concat filter（详情见：https://trac.ffmpeg.org/wiki/Concatenate）
            concat_clip_filename = self.current_path + str(instruction_set["flow_id"]) + "_clip_no_audio.mp4"

            ffmpeg.concat(
                *mat_clip_list
            ).output(
                concat_clip_filename
            ).run(
                cmd=self.ffmpeg_path,
                capture_stdout=True
            )

            self.tools_handle.assert_file_exist(concat_clip_filename)

            # 叠加音频轨道，输出最终成片，成片名称示例：1_output.mp4
            add_audio_set_list = [
                "./ffmpeg -i \"",
                self.current_path,
                str(instruction_set["flow_id"]),
                "_clip_no_audio.mp4\"",
                " -i \"",
                self.music_path,
                current_flow_detail["audio_path"],
                ".mp3\"",
                " -c copy \"",
                self.current_path,
                str(instruction_set["flow_id"]),
                "_output.mp4\"",
            ]

            add_audio_set = "".join(add_audio_set_list)
            print(add_audio_set)
            os.system(add_audio_set)

            self.tools_handle.assert_file_exist(self.current_path + str(instruction_set["flow_id"]) + "_output.mp4")

            # 更新流程表状态
            update_to_complete_render_sql = "update flow_distribute set status = '%s' where id = '%s' and status = '%s'" % \
                                            ("4", instruction_set["flow_id"], "3")

            self.db_handle.modify(update_to_complete_render_sql)

            # 到这一步，封面图和稿件本身都有了，开始准备分发（YouTube、Bilibili），同时把材料复制一份到仓库特定的文件夹，用来人肉分发（使用融媒宝分发各大平台）
            write_title, write_info = self.upload.distribute(
                instruction_set["flow_id"],
                json.loads(current_flow_detail["keywords"]),
                json.loads(current_flow_detail["adj_keywords"])
            )

            after_name = HSIS.main()
            shutil.copyfile(self.current_path + str(instruction_set["flow_id"]) + "_output.mp4", self.store_path + after_name + ".mp4")
            shutil.copyfile(self.current_path + str(instruction_set["flow_id"]) + "_cover.jpg", self.store_path + after_name + ".jpg")

            with open(self.store_path + after_name + ".txt", "w+") as temp_txt_file:
                temp_txt_file.writelines(write_title + "\n")
                temp_txt_file.writelines(write_info + "\n")
                temp_txt_file.writelines(current_flow_detail["keywords"] + "\n")
                temp_txt_file.writelines(current_flow_detail["adj_keywords"] + "\n")

            # TODO 测试通过，上线正式环境后，删除temp素材
            shutil.rmtree(current_clip_path)
            os.remove(self.current_path + str(instruction_set["flow_id"]) + "_output.mp4")
            os.remove(self.current_path + str(instruction_set["flow_id"]) + "_clip_no_audio.mp4")
            os.remove(self.current_path + str(instruction_set["flow_id"]) + "_cover.jpg")

            # 更新素材表记录，证明相关素材已经被分发，下次无需分发
            mat_id_list = [m["material_id"] for m in mat_list]
            update_mat_clip_sql = "update mat_clip set has_uploaded = '%s' where id in (%s)" % ("1", ','.join(['%s'] * len(mat_id_list)))
            self.db_handle.search(update_mat_clip_sql, mat_id_list)


if __name__ == '__main__':
    SERVER_IP = '127.0.0.1'
    rd = Render(SERVER_IP)
    rd.start()
