import cv2
import ffmpeg
import os

from utils.vision_algorithm.obtain_video_meta import meta_info
from utils.vision_algorithm.suitable_layout import fill, adapt, adapt_extra
from utils.id_generator import timestamp_gen

"""
@Author: Hocassian
@Date: 2022-09-15
@Info: 能用就行，不要试图搞懂该算法的原理
"""


class Horizontal2Vertical(object):

    def __init__(self):

        # 0正常处理 1四比三 2一比一
        self.frame_type = 1

        self.standard_1k_w = 1080
        self.standard_1k_h = 1920

        self.video_source_path = "temp_input/"  # 视频来源路径
        self.video_save_path = "temp_output/"  # 视频修改后的保存路径

    def blur_bg_cv2(self, file):

        capt = cv2.VideoCapture(self.video_source_path + file)

        # 采集原始素材信息
        origin_info, after_rate, origin_height, origin_width = meta_info(self.video_source_path + file)
        if all([
            origin_height == 0,
            origin_width == 0,
        ]):
            origin_height = int(capt.get(4))
            origin_width = int(capt.get(3))

        # Here, we are defining object to write the video and its location
        result = cv2.VideoWriter(
            self.video_save_path + self.filename + ".mp4",
            cv2.VideoWriter_fourcc('X', '2', '6', '4'),
            after_rate,
            (origin_height, origin_width)
        )

        while capt.isOpened():

            # We are capturing each frame of the video
            ret, frame = capt.read()
            if ret:
                # Here, we are performing our main task of blurring by adding gaussian blurring to the frame
                frame = cv2.GaussianBlur(frame, (25, 25), 0)
                # Here, we are saving the video frame
                result.write(frame)

            else:
                break

        capt.release()

    def blur_bg(self, file):

        # 采集原始素材信息
        origin_info, after_rate, origin_height, origin_width = meta_info(self.video_source_path + file)

        # 计算前景和背景尺寸
        tw1, th1, cw1, ch1, cw2, ch2 = fill(origin_width, origin_height, self.standard_1k_w, self.standard_1k_h)
        tw2, th2, lw, lh = adapt(origin_width, origin_height, self.standard_1k_w, self.standard_1k_h)

        # 去除一些不必要的处理
        if all([
            origin_width == tw1,
            origin_height == th1,
        ]):
            return

        # 如果frame_type有变动，就调整一下再传回来
        if self.frame_type != 0:
            tw2, th2, lw, lh, cx, cy, fw, fh = adapt_extra(
                origin_width,
                origin_height,
                self.standard_1k_w,
                self.standard_1k_h,
                self.frame_type,
            )

            # 开始合成
            cur_file = ffmpeg.input(self.video_source_path + file)
            fv1 = cur_file.video.filter("scale", tw1, th1).filter(
                "crop",
                self.standard_1k_w,
                self.standard_1k_h,
                cw1,
                ch1,
            ).filter("gblur", sigma=20)
            fv2 = cur_file.video.filter(
                "crop",
                fw,
                fh,
                cx,
                cy,
            ).filter("scale", tw2, th2)
            fa = cur_file.audio
            fv3 = ffmpeg.filter([fv1, fv2], 'overlay', lw, lh)
            out = ffmpeg.output(fv3, fa, self.video_save_path + str(timestamp_gen()) + ".mp4")
            out.run()

        else:

            # 开始合成
            cur_file = ffmpeg.input(self.video_source_path + file)
            fv1 = cur_file.video.filter("scale", tw1, th1).filter(
                "crop",
                self.standard_1k_w,
                self.standard_1k_h,
                cw1,
                ch1,
            ).filter("gblur", sigma=20)
            fv2 = cur_file.video.filter("scale", tw2, th2)
            fa = cur_file.audio
            fv3 = ffmpeg.filter([fv1, fv2], 'overlay', lw, lh)
            out = ffmpeg.output(fv3, fa, self.video_save_path + str(timestamp_gen()) + ".mp4")
            out.run()

    def run(self):
        for file in os.listdir(self.video_source_path):
            image_ext = ['.mp4', '.avi', '.mpg', '.mov']
            if os.path.splitext(file)[-1] in image_ext:
                self.blur_bg(file)


if __name__ == "__main__":
    hv = Horizontal2Vertical()
    hv.run()
