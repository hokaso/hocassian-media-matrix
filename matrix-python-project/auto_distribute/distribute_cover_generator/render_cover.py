import sys, os, random

sys.path.append(os.getcwd())
import time, json, pymysql
from PIL import Image

class RenderCover(object):

    def __init__(self):

        self.gen_pic_path = "auto_distribute/distribute_cover_generator/"
        self.gen_font_path = ""

    def main(self, thumbnail, fin_keywords_list, flow_id):

        # 生成背景板（例如：1_cover_background.png）
        cover_bg = self.thumbnail2cover(thumbnail)
        # cover_bg.save(os.path.join(self.gen_pic_path, str(flow_id) + '_cover_background.jpg'), quality=100)

        # 生成文字层（例如：1_cover_structure.png）
        structure_bg = self.render_structure(fin_keywords_list)

        # 贴合，合成封面图
        r, g, b, a = structure_bg.split()
        cover_bg.paste(structure_bg, (0, 0), mask=a)
        current_pic_path = self.gen_pic_path + str(flow_id) + '_cover.jpg'
        cover_bg.save(current_pic_path, quality=100)
        return current_pic_path

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

        return bg


    # 传入3个关键字，并渲染出对应封面结构图
    def render_structure(self, fin_keywords_list):

        # TODO 准备好文字层的底层模板

        bg = Image.open(self.gen_pic_path + "background.png")
        random.shuffle(fin_keywords_list)

        # 将tag关键字用「 / 」组合，总体长度不超过8个字符，如果超过，就只选两个（）

        # 随机三个形容关键字（免版权、4K、高清、可商用、HLG、10bit、60fps）

        return bg