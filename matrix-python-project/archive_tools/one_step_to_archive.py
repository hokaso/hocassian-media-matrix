# 问：给你若干个形式多种多样的视频，请写算法自动整理合并这些视频，保证尽可能小的冗余系数
# 答：将这些视频按多种标准分别合并，比如(,720P]的归档成一个（帧率30），
# (720P,2160P)归档成两个（帧率30&60），(2160P,)归档成两个（帧率30&60），
# 如果出现尺寸不符合16:9的，缩放为帧大小，其余地方用白色填补，按照最长边翻转为宽。
import sys, os, json, shutil, math, traceback, shlex, subprocess, ffmpeg

sys.path.append(os.getcwd())
from utils.tools import Tools
from archive_tools.spin_video import SpinVideo
from archive_tools.HMM_rate_archive_standard import HMM


class ArchiveAssistant(object):

    def __init__(self):

        with open(os.getcwd() + "/archive_tools/archive_config.json", 'r') as f0:
            info = json.load(f0)

        self.sv = SpinVideo()
        self.hmm = HMM()
        self.tools_handle = Tools()

        self.input_path = info["input_path"]
        self.output_path = info["output_path"]
        self.archive_path = info["archive_path"]
        self.ffmpeg_path = info["ffmpeg_path"]
        self.current_path = "archive_tools/"

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
        self.s1080r30_list = []
        self.s1080r60_list = []
        self.s2160r30_list = []
        self.s2160r60_list = []

        self.s720r30_ext = "_s720r30.mp4"
        self.s1080r30_ext = "_s1080r30.mp4"
        self.s1080r60_ext = "_s1080r60.mp4"
        self.s2160r30_ext = "_s2160r30.mp4"
        self.s2160r60_ext = "_s2160r60.mp4"

    def clip_classify(self):

        print(self)

    def clip_init(self):

        for clip in os.listdir(self.input_path):
            if os.path.isfile(clip):

                temp_origin_clip_path = self.input_path + clip
                clip_name, clip_extension = os.path.splitext(temp_origin_clip_path)

                # 采集原始素材信息
                catch_set = f'ffprobe -of json -select_streams v -show_streams "{temp_origin_clip_path}"'
                catch_json = subprocess.run(
                    shlex.split(catch_set),
                    capture_output=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                origin_info = json.loads(catch_json.stdout)
                if not origin_info['streams'][0]['height']:
                    print(temp_origin_clip_path + " is not a valid clip!")
                    continue

                origin_height = origin_info['streams'][0]['height']
                origin_width = origin_info['streams'][0]['width']

                tw, th, lw, lh, is_spin, resolution_standard = self.crop_to_suit(int(origin_width), int(origin_height))

                # 如果需旋转，则需要多做一步处理
                if is_spin:
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

                current_clip_path = clip_name + "_clip.mp4"

                temp_clip_set_list = [
                    "ffmpeg",
                    " -i \"",
                    temp_origin_clip_path,
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
                    "\" -crf ",
                    self.crf_map[resolution_standard],
                    " -s ",
                    str(resolution_standard[0]),
                    "x",
                    str(resolution_standard[1]),
                    " -r ",
                    str(after_rate),
                    " \"",
                    current_clip_path,
                    "\""
                ]

                temp_clip_set = "".join(temp_clip_set_list)
                print(temp_clip_set)
                os.system(temp_clip_set)

                # 校验文件是否存在
                if not os.path.isfile(current_clip_path):
                    print("无法处理片段：" + current_clip_path)
                    continue

                if after_rate == 30 and resolution_standard == self.s720:
                    self.s720r30_list.append(ffmpeg.input(current_clip_path))
                elif after_rate == 30 and resolution_standard == self.s1080:
                    self.s1080r30_list.append(ffmpeg.input(current_clip_path))
                elif after_rate == 60 and resolution_standard == self.s1080:
                    self.s1080r60_list.append(ffmpeg.input(current_clip_path))
                elif after_rate == 30 and resolution_standard == self.s2160:
                    self.s2160r30_list.append(ffmpeg.input(current_clip_path))
                elif after_rate == 60 and resolution_standard == self.s2160:
                    self.s2160r60_list.append(ffmpeg.input(current_clip_path))
                else:
                    self.s1080r30_list.append(ffmpeg.input(current_clip_path))

                # 最后将源文件移动到archive_path
                shutil.move(temp_origin_clip_path, self.archive_path + clip)

        self.concat(self.s720r30_list, self.output_path + self.s720r30_ext)
        self.concat(self.s1080r30_list, self.output_path + self.s1080r30_ext)
        self.concat(self.s1080r60_list, self.output_path + self.s1080r60_ext)
        self.concat(self.s2160r30_list, self.output_path + self.s2160r30_ext)
        self.concat(self.s2160r60_list, self.output_path + self.s2160r60_ext)

    def concat(self, clip_list, output_name):

        ffmpeg.concat(
            *clip_list
        ).output(
            output_name
        ).run(
            cmd=self.ffmpeg_path,
            capture_stdout=True
        )

        self.tools_handle.assert_file_exist(output_name)

    '''
    输入：
    fw和fh代表素材原本的宽高

    输出：
    resolution_standard表示渲染标准（1280、1920、3840对齐）
    is_spin表示是否需要旋转
    tw和th代表素材经过算法处理后的宽高
    lw和lh代表素材经过算法处理后左上角应该渲染在画面中的坐标（毕竟渲染器是从上至下，从左到右来渲染，所以需要左上角坐标）
    '''

    def crop_to_suit(self, fw, fh):

        # 确定is_spin、fw、fh
        is_spin = False
        if fw < fh * 16 / 9:
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

        # 确定tw和th
        tw = resolution_standard[0]
        th = math.ceil(resolution_standard[0] * fh / fw)

        # 确定lw和lh
        lw = int((FOUR_KILO_W - tw) / 2)
        lh = int((FOUR_KILO_H - th) / 2)

        return tw, th, lw, lh, is_spin, resolution_standard
