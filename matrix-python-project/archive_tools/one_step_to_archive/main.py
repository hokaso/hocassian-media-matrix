# 问：给你若干个形式多种多样的视频，请写算法自动整理合并这些视频，保证尽可能小的冗余系数
# 答：将这些视频按多种标准分别合并，比如(,720P]的归档成一个（帧率30），
# (720P,2160P)归档成两个（帧率30&60），(2160P,)归档成两个（帧率30&60），
# 如果出现尺寸不符合16:9的，缩放为帧大小，其余地方用白色填补，按照最长边翻转为宽。
import sys, os, json, shutil, math, shlex, subprocess, ffmpeg, traceback

sys.path.append(os.getcwd())
from utils.tools import Tools
from archive_tools.tools.spin_video import SpinVideo
from archive_tools.tools.rate_archive_standard import HMM
from utils.snow_id import HSIS

# 仅适用于linux系统
class ArchiveAssistant(object):

    def __init__(self):

        with open("archive_tools/one_step_to_archive/config/archive_config.json", 'r') as f0:
            info = json.load(f0)

        self.sv = SpinVideo()
        self.hmm = HMM()
        self.tools_handle = Tools()

        self.input_path = info["input_path"]
        self.output_path = info["output_path"]
        self.archive_path = info["archive_path"]
        self.ffmpeg_path = info["ffmpeg_path"]
        self.current_path = "archive_tools/one_step_to_archive/materials/"

        self.s720 = (1280, 720)
        self.s1080 = (1920, 1080)
        self.s2160 = (3840, 2160)

        s720_bg = self.current_path + "clip_bg_720.png"
        s1080_bg = self.current_path + "clip_bg_1080.png"
        s2160_bg = self.current_path + "clip_bg_2160.png"

        self.bg_map = {
            self.s720: s720_bg,
            self.s1080: s1080_bg,
            self.s2160: s2160_bg,
        }

        self.crf_map = {
            self.s720: "26",
            self.s1080: "22",
            self.s2160: "20",
        }

        self.s720r30_list = []
        self.s720r60_list = []
        self.s1080r30_list = []
        self.s1080r60_list = []
        self.s2160r30_list = []
        self.s2160r60_list = []

        self.s720r30_list_file = []
        self.s720r60_list_file = []
        self.s1080r30_list_file = []
        self.s1080r60_list_file = []
        self.s2160r30_list_file = []
        self.s2160r60_list_file = []

        self.s720r30_ext = "s720r30"
        self.s720r60_ext = "s720r60"
        self.s1080r30_ext = "s1080r30"
        self.s1080r60_ext = "s1080r60"
        self.s2160r30_ext = "s2160r30"
        self.s2160r60_ext = "s2160r60"

    def clip_classify(self):

        for clip in os.listdir(self.input_path):
            temp_origin_clip_path = self.input_path + "/" + clip
            print(temp_origin_clip_path)
            if os.path.isfile(temp_origin_clip_path):

                # 采集原始素材信息
                catch_set = f'ffprobe -of json -select_streams v -show_streams "{temp_origin_clip_path}"'
                catch_json = subprocess.run(
                    shlex.split(catch_set),
                    capture_output=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                origin_info = json.loads(catch_json.stdout)
                print(origin_info)
                try:
                    if origin_info == {} or "streams" not in origin_info or not origin_info['streams'][0]['height']:
                        print(temp_origin_clip_path + " is not a valid clip!")
                        continue
                except Exception as e:
                    print(temp_origin_clip_path + " is not a valid clip!")
                    traceback.print_exc()
                    print(e)
                    continue

                origin_height = origin_info['streams'][0]['height']
                origin_width = origin_info['streams'][0]['width']

                tw, th, lw, lh, is_spin, resolution_standard = self.crop_to_suit(int(origin_width), int(origin_height),
                                                                                 False)

                # 确定渲染帧率
                if 'avg_frame_rate' in origin_info['streams'][0]:
                    pix_rate = origin_info['streams'][0]['avg_frame_rate']
                    after_rate = self.hmm.archive_standard(eval(pix_rate))
                else:
                    # 默认30fps
                    after_rate = 30

                current_clip_path_with_ext = temp_origin_clip_path
                if after_rate == 30 and resolution_standard == self.s720:
                    self.s720r30_list.append(ffmpeg.input(current_clip_path_with_ext))
                    self.s720r30_list_file.append(current_clip_path_with_ext)
                elif after_rate == 60 and resolution_standard == self.s720:
                    self.s720r60_list.append(ffmpeg.input(current_clip_path_with_ext))
                    self.s720r60_list_file.append(current_clip_path_with_ext)
                elif after_rate == 30 and resolution_standard == self.s1080:
                    self.s1080r30_list.append(ffmpeg.input(current_clip_path_with_ext))
                    self.s1080r30_list_file.append(current_clip_path_with_ext)
                elif after_rate == 60 and resolution_standard == self.s1080:
                    self.s1080r60_list.append(ffmpeg.input(current_clip_path_with_ext))
                    self.s1080r60_list_file.append(current_clip_path_with_ext)
                elif after_rate == 30 and resolution_standard == self.s2160:
                    self.s2160r30_list.append(ffmpeg.input(current_clip_path_with_ext))
                    self.s2160r30_list_file.append(current_clip_path_with_ext)
                elif after_rate == 60 and resolution_standard == self.s2160:
                    self.s2160r60_list.append(ffmpeg.input(current_clip_path_with_ext))
                    self.s2160r60_list_file.append(current_clip_path_with_ext)
                # else:
                #     self.s1080r30_list.append(ffmpeg.input(current_clip_path_with_ext))

        self.concat(self.s720r30_list, self.s720r30_list_file, self.output_path + self.s720r30_ext,
                    self.crf_map[self.s720])
        self.concat(self.s720r60_list, self.s720r60_list_file, self.output_path + self.s720r60_ext,
                    self.crf_map[self.s720])
        self.concat(self.s1080r30_list, self.s1080r30_list_file, self.output_path + self.s1080r30_ext,
                    self.crf_map[self.s1080])
        self.concat(self.s1080r60_list, self.s1080r60_list_file, self.output_path + self.s1080r60_ext,
                    self.crf_map[self.s1080])
        self.concat(self.s2160r30_list, self.s2160r30_list_file, self.output_path + self.s2160r30_ext,
                    self.crf_map[self.s2160])
        self.concat(self.s2160r60_list, self.s2160r60_list_file, self.output_path + self.s2160r60_ext,
                    self.crf_map[self.s2160])

    def clip_init(self):

        for clip in os.listdir(self.input_path):
            temp_origin_clip_path = self.input_path + "/" + clip
            if os.path.isfile(temp_origin_clip_path):
                # clip_name, clip_extension = os.path.splitext(temp_origin_clip_path)

                # 采集原始素材信息
                catch_set = f'ffprobe -of json -select_streams v -show_streams "{temp_origin_clip_path}"'
                catch_json = subprocess.run(
                    shlex.split(catch_set),
                    capture_output=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                origin_info = json.loads(catch_json.stdout)
                print(origin_info)
                if origin_info == {} or "streams" not in origin_info or not origin_info['streams'][0]['height']:
                    print(temp_origin_clip_path + " is not a valid clip!")
                    continue

                origin_height = origin_info['streams'][0]['height']
                origin_width = origin_info['streams'][0]['width']

                extra_is_spin = False
                if "side_data_list" in origin_info['streams'][0] and origin_info['streams'][0]["side_data_list"] != 0:
                    extra_is_spin = True

                # 初步确定素材类别（后期可手动调整）
                is_HDR_and_vertical = False
                if 'pix_fmt' in origin_info['streams'][0]:
                    origin_pix_fmt = origin_info['streams'][0]['pix_fmt']
                    if origin_pix_fmt == 'yuv422p10le' and extra_is_spin:
                        is_HDR_and_vertical = True

                tw, th, lw, lh, is_spin, resolution_standard = self.crop_to_suit(int(origin_width), int(origin_height),
                                                                                 is_HDR_and_vertical)

                # 如果需旋转，则需要多做一步处理
                if (is_spin or extra_is_spin) and not is_HDR_and_vertical:
                    is_success = self.sv.get_cmd(temp_origin_clip_path)
                    if not is_success:
                        print("无法处理片段：" + temp_origin_clip_path)
                        continue

                # 确定渲染帧率
                if 'avg_frame_rate' in origin_info['streams'][0]:
                    pix_rate = origin_info['streams'][0]['avg_frame_rate']
                    after_rate = self.hmm.archive_standard(eval(pix_rate))
                else:
                    # 默认30fps
                    after_rate = 30

                # 設定唯一id
                after_name = HSIS.main()
                current_clip_path = self.input_path + "/" + after_name + "_clip"

                # 首次處理幀率
                rate_set_list = [
                    "ffmpeg -r ",
                    str(after_rate),
                    " -i ",
                    "\"",
                    temp_origin_clip_path,
                    "\"",
                    " -crf ",
                    self.crf_map[resolution_standard],
                    " \"",
                    current_clip_path,
                    "_.mp4",
                    "\""
                ]
                rate_set = "".join(rate_set_list)
                print(rate_set)
                os.system(rate_set)

                # 校验文件是否存在
                if not os.path.isfile(current_clip_path + "_.mp4"):
                    print("无法处理片段：" + current_clip_path + "_.mp4")
                    continue

                # 二次處理畫面
                temp_clip_set_list = [
                    "ffmpeg",
                    " -i \"",
                    current_clip_path,
                    "_.mp4",
                    "\" -i \"",
                    self.bg_map[resolution_standard],
                    "\" ",
                    "-filter_complex \"[0:v]scale=",
                    str(tw),
                    ":",
                    str(th),
                    "[video1];[1:v][video1]overlay=",
                    str(lw),
                    ":",
                    str(lh),
                    "\"",
                    " -crf ",
                    self.crf_map[resolution_standard],
                    " -s ",
                    str(resolution_standard[0]),
                    "x",
                    str(resolution_standard[1]),
                    " -r ",
                    str(after_rate),
                    " \"",
                    current_clip_path,
                    ".mp4",
                    "\""
                ]

                temp_clip_set = "".join(temp_clip_set_list)
                print(temp_clip_set)
                os.system(temp_clip_set)

                # 校验文件是否存在
                if not os.path.isfile(current_clip_path + ".mp4"):
                    print("无法处理片段：" + current_clip_path + ".mp4")
                    continue

                # 刪除舊文件並改名
                os.remove(current_clip_path + "_.mp4")

                # current_clip_path_with_ext = current_clip_path + ".mp4"
                # if after_rate == 30 and resolution_standard == self.s720:
                #     self.s720r30_list.append(ffmpeg.input(current_clip_path_with_ext))
                #     self.s720r30_list_file.append(current_clip_path_with_ext)
                # elif after_rate == 30 and resolution_standard == self.s1080:
                #     self.s1080r30_list.append(ffmpeg.input(current_clip_path_with_ext))
                #     self.s1080r30_list_file.append(current_clip_path_with_ext)
                # elif after_rate == 60 and resolution_standard == self.s1080:
                #     self.s1080r60_list.append(ffmpeg.input(current_clip_path_with_ext))
                #     self.s1080r60_list_file.append(current_clip_path_with_ext)
                # elif after_rate == 30 and resolution_standard == self.s2160:
                #     self.s2160r30_list.append(ffmpeg.input(current_clip_path_with_ext))
                #     self.s2160r30_list_file.append(current_clip_path_with_ext)
                # elif after_rate == 60 and resolution_standard == self.s2160:
                #     self.s2160r60_list.append(ffmpeg.input(current_clip_path_with_ext))
                #     self.s2160r60_list_file.append(current_clip_path_with_ext)
                # else:
                #     self.s1080r30_list.append(ffmpeg.input(current_clip_path_with_ext))

                # 最后将源文件移动到archive_path
                shutil.move(temp_origin_clip_path, self.archive_path + "/" + clip)

        # self.concat(self.s720r30_list, self.s720r30_list_file, self.output_path + self.s720r30_ext, self.crf_map[self.s720])
        # self.concat(self.s1080r30_list, self.s1080r30_list_file, self.output_path + self.s1080r30_ext, self.crf_map[self.s1080])
        # self.concat(self.s1080r60_list, self.s1080r60_list_file, self.output_path + self.s1080r60_ext, self.crf_map[self.s1080])
        # self.concat(self.s2160r30_list, self.s2160r30_list_file, self.output_path + self.s2160r30_ext, self.crf_map[self.s2160])
        # self.concat(self.s2160r60_list, self.s2160r60_list_file, self.output_path + self.s2160r60_ext, self.crf_map[self.s2160])

    # Tips：每个合集的视频片段大小不应超过8G，否则会造成内存溢出（默认服务器内存为128G）。
    def concat(self, clip_list, clip_list_file, output_name, crf):
        try:
            if clip_list:

                # 增加分段处理，每100个视频片段应该归为一组
                cluster_num = len(clip_list) // 100
                if cluster_num == 0:
                    self.concat_sku(clip_list, output_name + ".mp4", crf)

                for ikey in range(cluster_num):
                    fin_name = output_name + "-" + str(ikey) + ".mp4"
                    if ikey == cluster_num:
                        last_index = len(clip_list) - 1
                    else:
                        last_index = ikey*100+99

                    temp_cluster_list = clip_list[ikey*100:last_index]

                    self.concat_sku(temp_cluster_list, fin_name, crf)

                for d_key in clip_list_file:
                    os.remove(d_key)

        except Exception as e:
            traceback.print_exc()
            print(e)
            return "fail"

    def concat_sku(self, temp_cluster_list, fin_name, crf):

        ffmpeg.concat(
            *temp_cluster_list
        ).output(
            fin_name,
            crf=int(crf)
        ).run(
            cmd=self.ffmpeg_path,
            capture_stdout=True
        )

        self.tools_handle.assert_file_exist(fin_name)


    '''
    输入：
    fw和fh代表素材原本的宽高

    输出：
    resolution_standard表示渲染标准（1280、1920、3840对齐）
    is_spin表示是否需要旋转
    tw和th代表素材经过算法处理后的宽高
    lw和lh代表素材经过算法处理后左上角应该渲染在画面中的坐标（毕竟渲染器是从上至下，从左到右来渲染，所以需要左上角坐标）
    '''

    def crop_to_suit(self, fw, fh, is_HDR_and_vertical):

        # 确定is_spin、fw、fh
        is_spin = False
        if fw < fh:
            # 长边恒为宽
            fw, fh = fh, fw
            is_spin = True

        # 确定resolution_standard
        if fw <= self.s720[0]:
            resolution_standard = self.s720
        elif fw < self.s2160[0]:
            resolution_standard = self.s1080
        elif fw >= self.s2160[0]:
            resolution_standard = self.s2160
        else:
            resolution_standard = self.s1080

        # 当视频为特殊格式时，保持宽高，两侧留白（ffmpeg不支持旋轉這類視頻）
        if is_HDR_and_vertical:
            fw, fh = fh, fw
            th = resolution_standard[1]
            tw = math.ceil(resolution_standard[1] * fw / fh)
            is_spin = False
        else:
            # 确定tw和th
            tw = resolution_standard[0]
            th = math.ceil(resolution_standard[0] * fh / fw)

        # 确定lw和lh
        lw = int((resolution_standard[0] - tw) / 2)
        lh = int((resolution_standard[1] - th) / 2)

        return tw, th, lw, lh, is_spin, resolution_standard

# 使用逻辑，先取消aa.clip_init()的注释，全部素材刷一遍，统一规格，然后取消aa.clip_classify()的注释，把aa.clip_init()注释回去，把错误的挑出来删掉，然后重试；
if __name__ == '__main__':
    aa = ArchiveAssistant()
    aa.clip_init()
    aa.clip_classify()
