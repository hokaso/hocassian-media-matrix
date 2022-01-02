import sys, os, math

sys.path.append(os.getcwd())
import time
from PIL import Image, ImageFilter


class GenImg(object):

    def __init__(self):
        
        self.standard_1k_w = 1920
        self.standard_1k_h = 1080

        self.img_source_path = "temp_input/"  # 图片来源路径
        self.img_save_path = "temp_output/"  # 图片修改后的保存路径

    # 封面图标准：1920*1080，边边角角之类的通过背后叠一层模糊图层来解决
    def thumbnail2cover(self, thumbnail):

        img = Image.open(thumbnail)
        w, h = img.size
        if w >= h * 16 / 9:
            re_bg_w = math.ceil(self.standard_1k_h * w / h)
            re_bg_h = self.standard_1k_h
            re_fg_w = self.standard_1k_w
            re_fg_h = math.ceil(self.standard_1k_w * h / w)
        else:
            re_bg_w = self.standard_1k_w
            re_bg_h = math.ceil(self.standard_1k_w * h / w)
            re_fg_h = self.standard_1k_h
            re_fg_w = math.ceil(self.standard_1k_h * w / h)

        # 把原图放大为背景图
        back_img_tmp = img.resize((re_bg_w, re_bg_h), Image.ANTIALIAS)

        # 把原图处理成前景图
        img2 = img.resize((re_fg_w, re_fg_h), Image.ANTIALIAS)
        bg_point_x = int((re_bg_w - self.standard_1k_w) / 2)
        bg_point_y = int((re_bg_h - self.standard_1k_h) / 2)

        # 裁切背景图
        back_img_tmp2 = back_img_tmp.crop(
            [bg_point_x, bg_point_y, bg_point_x + self.standard_1k_w, bg_point_y + self.standard_1k_h])

        # 模糊背景图
        img = back_img_tmp2.filter(ImageFilter.GaussianBlur(radius=18))
        fg_point_x = int((self.standard_1k_w - re_fg_w) / 2)
        fg_point_y = int((self.standard_1k_h - re_fg_h) / 2)

        # 拼合
        img.paste(img2, (fg_point_x, fg_point_y, fg_point_x + re_fg_w, fg_point_y + re_fg_h))

        # 这两步是用来转换的
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img)

        return bg


    def run(self):
        for file in os.listdir(self.img_source_path):
            x = self.thumbnail2cover(self.img_source_path + file)
            new_pic_name = int(round(time.time() * 1000))
            x.save(os.path.join(self.img_save_path, str(new_pic_name) + '.jpg'), quality=100)


if __name__ == '__main__':
    GenImg().run()