import sys, os

sys.path.append(os.getcwd())
import time, json, pymysql
from PIL import Image

class RenderCover(object):

    def main(self, thumbnail, fin_keywords_list):

        # 生成背景板
        self.thumbnail2cover(thumbnail)
        # 生成文字层

        # 贴合，合成封面图


    # 封面图标准：1920*1080，边边角角之类的通过背后叠一层模糊图层来解决
    @staticmethod
    def thumbnail2cover(thumbnail):

        img = Image.open(thumbnail)
        w, h = img.size
        if w >= h * 16 / 9:
            re_bg_w = math.ceil(1080 * w / h)
            re_bg_h = 1080
            re_fg_w = 1920
            re_fg_h = math.ceil(1920 * h / w)
        else:
            re_bg_w = 1920
            re_bg_h = math.ceil(1920 * h / w)
            re_fg_h = 1080
            re_fg_w = math.ceil(1080 * w / h)

        # 把原图放大为背景图
        back_img_tmp = img.resize((re_bg_w, re_bg_h), Image.ANTIALIAS)

        # 把原图处理成前景图
        img2 = img.resize((re_fg_w, re_fg_h), Image.ANTIALIAS)
        bg_pointx = int((re_bg_w - 1920) / 2)
        bg_pointy = int((re_bg_h - 1080) / 2)

        # 裁切背景图
        back_img_tmp2 = back_img_tmp.crop([bg_pointx, bg_pointy, bg_pointx + 1920, bg_pointy + 1080])

        # 模糊背景图
        img = back_img_tmp2.filter(ImageFilter.GaussianBlur(radius=18))
        fg_pointx = int((1920 - re_fg_w) / 2)
        fg_pointy = int((1080 - re_fg_h) / 2)

        # 拼合
        img.paste(img2, (fg_pointx, fg_pointy, fg_pointx + re_fg_w, fg_pointy + re_fg_h))

        # 这两步是用来转换的
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img)