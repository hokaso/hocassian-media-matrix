import os
from typing import List, Tuple

from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors.content_detector import ContentDetector
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.video_splitter import split_video_ffmpeg


def clip_render(clip_name, scenes, crf, output_dir):
    print(scenes)
    file_path, full_name = os.path.split(clip_name)
    f_name, ext = os.path.splitext(full_name)
    split_video_ffmpeg(
        clip_name,
        scenes,
        "$VIDEO_NAME - Scene $SCENE_NUMBER.mp4",
        output_dir + f_name,
        arg_override='-c:v libx264 -preset medium -crf ' + str(crf) + ' -c:a aac',
        show_progress=True,
        show_output=False
    )


def modify_scene_list(
        base_scene: tuple[FrameTimecode, FrameTimecode],
) -> List[Tuple[FrameTimecode, FrameTimecode]]:
    return [(FrameTimecode(base_scene[0] + 1), FrameTimecode(base_scene[1] - 1))]


def find_scenes(video_manager, threshold):
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    base_timecode = video_manager.get_base_timecode()

    try:

        video_manager.set_downscale_factor()
        video_manager.start()

        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list(base_timecode)
        final_scene_list = []
        for scene in scene_list:
            final_scene_list += modify_scene_list(scene)

    finally:
        video_manager.release()

    return final_scene_list


class DynamicInterval(object):
    pass


if __name__ == "__main__":
    video_path = ""
    video = VideoManager([video_path])
    di = DynamicInterval()
    find_scenes(video_manager=video, threshold=27.5)
