# 在使用前，请通过「pip install scenedetect[opencv,progress_bar,scenedetect]」安装部分所需要的依赖~

from __future__ import print_function
import os

# Standard PySceneDetect imports:
from scenedetect.video_splitter import split_video_ffmpeg
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
# For caching detection metrics and saving/loading to a stats file
from scenedetect.stats_manager import StatsManager

# For content-aware scene detection:
from scenedetect.detectors.content_detector import ContentDetector

class AutoClip(object):

    def __init__(self):

        self.input_dir = './input'
        self.output_dir = 'output'

        self.current_clip_output_path = os.getcwd() + "/" + self.output_dir
        if not os.path.exists(self.current_clip_output_path):
            os.makedirs(self.current_clip_output_path)

        self.threshold_default = 27.5
        self.crf_default = 20


    def run(self):
        _file_list = self.file_prepare()
        threshold = input("请输入画面阈值（选择区间[10, 90]，如无输入则默认27.5）：")
        if not threshold:
            threshold = self.threshold_default

        crf = input("请输入crf值（选择区间[1, 51]，如无输入则默认20）：")
        if not crf:
            crf = self.crf_default

        for key in _file_list:
            scenes = self.find_scenes(key, threshold)
            print(scenes)
            file_path, full_name = os.path.split(key)
            f_name, ext = os.path.splitext(full_name)
            split_video_ffmpeg(
                [key],
                scenes,
                "$VIDEO_NAME - Scene $SCENE_NUMBER.mp4",
                self.output_dir + "/" + f_name,
                arg_override='-c:v libx264 -preset slow -crf ' + str(crf) + ' -c:a aac',
                hide_progress=False,
                suppress_output=False
            )

        print("处理完毕~")

    @staticmethod
    def find_scenes(video_path, threshold):
        video_manager = VideoManager([video_path])
        stats_manager = StatsManager()
        # Construct our SceneManager and pass it our StatsManager.
        scene_manager = SceneManager(stats_manager)

        # Add ContentDetector algorithm (each detector's constructor
        # takes detector options, e.g. threshold).
        scene_manager.add_detector(ContentDetector(threshold=threshold))
        base_timecode = video_manager.get_base_timecode()

        try:

            # Set downscale factor to improve processing speed.
            video_manager.set_downscale_factor()

            # Start video_manager.
            video_manager.start()

            # Perform scene detection on video_manager.
            scene_manager.detect_scenes(frame_source=video_manager)

            # Obtain list of detected scenes.
            scene_list = scene_manager.get_scene_list(base_timecode)
            # Each scene is a tuple of (start, end) FrameTimecodes.

            print('List of scenes obtained:')
            final_scene_list = []
            for i, scene in enumerate(scene_list):
                temp = list(scene)
                # print(temp)
                temp[0] = temp[0] + 1
                temp[1] = temp[1] - 1
                scene = tuple(temp)
                final_scene_list.append(scene)

        finally:
            video_manager.release()

        return final_scene_list

    def file_prepare(self):
        file_list = []
        for root, dirs, files in os.walk(self.input_dir):
            file_list = [self.input_dir + "/" + i for i in files]
        return file_list

if __name__ == '__main__':
    AutoClip().run()