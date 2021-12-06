import sys, os, random, math

sys.path.append(os.getcwd())
import time, json
from PIL import Image, ImageFilter, ImageDraw, ImageFont


class RenderCover(object):

    def __init__(self):

        with open("auto_distribute/distribute_cover_generator/layout.json", 'r') as f0:
            self.info = json.load(f0)

        self.font_path = "auto_distribute/distribute_cover_generator/font/" + self.info["font"]
        self.material_pic_path = "auto_distribute/distribute_cover_generator/"
        self.gen_pic_path = "auto_distribute/"

        self.standard_1k_w = 1920
        self.standard_1k_h = 1080

    def main(self, thumbnail, fin_keywords_list, flow_id, adj_keywords):

        # 生成背景板（例如：1_cover_background.png）
        cover_bg = self.thumbnail2cover(thumbnail)
        # cover_bg.save(os.path.join(self.gen_pic_path, str(flow_id) + '_cover_background.jpg'), quality=100)

        # 生成文字层（例如：1_cover_structure.png）
        structure_bg = self.render_structure(fin_keywords_list, adj_keywords)

        # 贴合，合成封面图（例如：1_cover.jpg；如果分发流程有其他要求，再根据对应流程生成相应格式）
        r, g, b, a = structure_bg.split()
        cover_bg.paste(structure_bg, (0, 0), mask=a)
        current_pic_path = self.gen_pic_path + str(flow_id) + '_cover.jpg'
        cover_bg.save(current_pic_path, quality=100)
        return current_pic_path

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
        bg_pointx = int((re_bg_w - self.standard_1k_w) / 2)
        bg_pointy = int((re_bg_h - self.standard_1k_h) / 2)

        # 裁切背景图
        back_img_tmp2 = back_img_tmp.crop([bg_pointx, bg_pointy, bg_pointx + self.standard_1k_w, bg_pointy + self.standard_1k_h])

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

    # 传入3个关键字，并渲染出对应封面结构图
    def render_structure(self, fin_keywords_list, adj_keywords):

        # 准备好文字层的底层模板
        bg = Image.open(self.material_pic_path + "material_01.png")
        draw = ImageDraw.Draw(bg)

        # 取前三个tag渲染进封面图
        select_keywords_list = fin_keywords_list[:3]
        random.shuffle(select_keywords_list)

        # 将tag关键字用「·」组合，总体长度不超过8个字符，如果超过，就只选两个
        _render_tag = "·".join(select_keywords_list)
        if len(_render_tag) > 10:
            _render_tag = "·".join(select_keywords_list[:2])

        render_tag = "「" + _render_tag + "」"

        # 将形容关键字用「 / 」组合
        render_adj = " / ".join(adj_keywords)

        # 根据create时间生成底部版权声明
        render_time = time.strftime('%Y.%m.%d', time.localtime())

        # 加载字体
        tag_font = ImageFont.truetype(self.font_path, size=self.info["tag_size"])
        adj_font = ImageFont.truetype(self.font_path, size=self.info["adj_size"])
        time_font = ImageFont.truetype(self.font_path, size=self.info["time_size"])

        tag_location = draw.textsize(render_tag, font=tag_font)
        adj_location = draw.textsize(render_adj, font=adj_font)
        # time_location = draw.textsize(render_time, font=time_font)

        # 加载并按需拉伸阴影背景
        shadow_bg = Image.open(self.material_pic_path + "material_02.png")
        # shadow_w, shadow_h = shadow_bg.size

        tag_shadow_bg_location = self.spread_shadow(tag_location)
        tag_shadow_bg = shadow_bg.resize(tag_shadow_bg_location, Image.ANTIALIAS)

        adj_shadow_bg_location = self.spread_shadow(adj_location)
        adj_shadow_bg = shadow_bg.resize(adj_shadow_bg_location, Image.ANTIALIAS)

        # 阴影贴合到structure上
        tag_shadow_paste_x = (self.standard_1k_w - tag_shadow_bg_location[0]) / 2
        tag_shadow_paste_y = self.info["tag_top"] - (tag_shadow_bg_location[1] - tag_location[1]) / 2 + 15 # 修复计算误差
        r, g, b, a = tag_shadow_bg.split()
        bg.paste(tag_shadow_bg, (int(tag_shadow_paste_x), int(tag_shadow_paste_y)), mask=a)

        adj_shadow_paste_x = (self.standard_1k_w - adj_shadow_bg_location[0]) / 2
        adj_shadow_paste_y = self.info["adj_top"] - (adj_shadow_bg_location[1] - adj_location[1]) / 2
        r, g, b, a = adj_shadow_bg.split()
        bg.paste(adj_shadow_bg, (int(adj_shadow_paste_x), int(adj_shadow_paste_y)), mask=a)

        # 文字贴合到structure上（包括文字阴影）
        tag_paste_x = int((self.standard_1k_w - tag_location[0]) / 2)
        tag_paste_y = self.info["tag_top"]

        draw.text(
            (
                tag_paste_x + self.info["tag_shadow_offset"][0],
                tag_paste_y + self.info["tag_shadow_offset"][1]
            ),
            render_tag,
            font=tag_font,
            fill=tuple(eval(self.info["tag_shadow_fill"]))
        )
        draw.text(
            (tag_paste_x, tag_paste_y),
            render_tag,
            font=tag_font,
            fill=tuple(eval(self.info["tag_color"]))
        )

        adj_paste_x = int((self.standard_1k_w - adj_location[0]) / 2)
        adj_paste_y = self.info["adj_top"]

        draw.text(
            (
                adj_paste_x + self.info["adj_shadow_offset"][0],
                adj_paste_y + self.info["adj_shadow_offset"][1]
            ),
            render_adj,
            font=adj_font,
            fill=tuple(eval(self.info["adj_shadow_fill"]))
        )
        draw.text(
            (adj_paste_x, adj_paste_y),
            render_adj,
            font=adj_font,
            fill=tuple(eval(self.info["adj_color"]))
        )

        # 渲染时间
        time_paste_x = self.info["time_location"][0]
        time_paste_y = self.info["time_location"][1]

        draw.text(
            (time_paste_x, time_paste_y),
            render_time,
            font=time_font,
            fill=tuple(eval(self.info["time_color"]))
        )

        return bg

    def spread_shadow(self, location):
        print(location)
        new_location = (int(location[0] * self.info["shadow_spread_ratio_x"]), int(location[1] * self.info["shadow_spread_ratio_y"]))
        print(new_location)
        return new_location
