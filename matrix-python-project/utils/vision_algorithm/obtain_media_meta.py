import shlex
import subprocess
import os
import json

from PIL import Image
from utils.vision_algorithm.rate_archive_standard import archive_standard


def image_meta_info(filename):
    img = Image.open(filename)
    origin_width, origin_height = img.size
    origin_size = os.path.getsize(filename)
    return origin_width, origin_height, origin_size, img


def video_meta(filename):
    catch_set = f'ffprobe -of json -select_streams v -show_streams "{filename}"'
    catch_json = subprocess.run(
        shlex.split(catch_set),
        capture_output=True,
        encoding='utf-8',
        errors='ignore'
    )
    origin_info = json.loads(catch_json.stdout)

    return origin_info


def video_rate_info(origin_info):
    # 确定渲染帧率
    if 'avg_frame_rate' in origin_info['streams'][0]:
        pix_rate = origin_info['streams'][0]['avg_frame_rate']
        after_rate = archive_standard(eval(pix_rate))
    else:
        # 默认30fps
        after_rate = 30

    return after_rate


def video_is_ten_bit(origin_info):
    if 'pix_fmt' in origin_info['streams'][0]:
        origin_pix_fmt = origin_info['streams'][0]['pix_fmt']
        if origin_pix_fmt == 'yuv422p10le':
            return True
    return False


def video_is_bt2020(origin_info):
    if 'color_primaries' in origin_info['streams'][0]:
        origin_pix_fmt = origin_info['streams'][0]['color_primaries']
        if origin_pix_fmt == 'bt2020':
            return True
    return False


def video_meta_info(filename):
    # 采集原始素材信息
    origin_info = video_meta(filename)

    # 确定渲染帧率
    if 'avg_frame_rate' in origin_info['streams'][0]:
        pix_rate = origin_info['streams'][0]['avg_frame_rate']
        after_rate = archive_standard(eval(pix_rate))
    else:
        # 默认30fps
        after_rate = 30

    # 确定视频宽高
    origin_height = 0
    origin_width = 0
    if "streams" in origin_info:
        origin_height = origin_info['streams'][0]['height']
        origin_width = origin_info['streams'][0]['width']

    # 持续时间（单位：秒）
    origin_duration = float(origin_info['streams'][0]['duration'])

    return origin_width, origin_height, origin_duration, after_rate


class ObtainVideoMeta(object):

    def __init__(self):
        print(self)

