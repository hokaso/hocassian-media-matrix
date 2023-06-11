import shlex
import subprocess
import json

from utils.vision_algorithm.rate_archive_standard import archive_standard


def meta_info(filename):
    # 采集原始素材信息
    catch_set = f'ffprobe -of json -select_streams v -show_streams "{filename}"'
    catch_json = subprocess.run(
        shlex.split(catch_set),
        capture_output=True,
        encoding='utf-8',
        errors='ignore'
    )
    origin_info = json.loads(catch_json.stdout)

    # 确定渲染帧率
    if 'avg_frame_rate' in origin_info['streams'][0]:
        pix_rate = origin_info['streams'][0]['avg_frame_rate']
        after_rate = archive_standard(eval(pix_rate))
    else:
        # 默认30fps
        after_rate = 30

    origin_height = 0
    origin_width = 0
    if "streams" in origin_info:
        origin_height = origin_info['streams'][0]['height']
        origin_width = origin_info['streams'][0]['width']

    return origin_info, after_rate, origin_height, origin_width


class ObtainVideoMeta(object):

    def __init__(self):
        print(self)

