import sys, os, time, json, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.append(os.getcwd())


class Structure(object):

    def __init__(self):
        self.first_title = None
        self.secord_title = None

        self.font_path = "cover_generator/font"

        with open("cover_generator/layout.json", 'r') as f0:
            self.layout_config = json.load(f0)

        self.tb = Image.open("cover_generator/" + self.layout_config["transparent_background"])

        # 「4+1」模型：0传统、1简约、2科技、3简洁
        # 「3中」模型：4诙谐、5古典、6纵横、7聚焦、8清新
        self.structure_map = {
            0: self.traditional,
            1: self.simplicity,
            2: self.technology,
            3: self.simplify,
            4: self.humorous,
            5: self.classical,
            6: self.vertical,
            7: self.focus,
            8: self.fresh
        }

        self.x_model_map = {
            0: "○",
            1: "↖",
            2: "↙",
            3: "↗",
            4: "↘",
        }

        self.l_model_map = {
            0: "↑",
            1: "○",
            2: "↓",
        }

    def model_init(
            self,
            config
    ):

        # 加载模板为可绘制对象
        draw = ImageDraw.Draw(self.tb)

        # 随机字体
        current_font = self.random_font()
        first_title_font = ImageFont.truetype("cover_generator/font/" + current_font, size=config["text"][0]["size"])
        secord_title_font = ImageFont.truetype("cover_generator/font/" + current_font, size=config["text"][1]["size"])

        # 计算文字相对位置
        first_title_size = draw.textsize(self.first_title, font=first_title_font)
        secord_title_size = draw.textsize(self.secord_title, font=secord_title_font)

        return draw, first_title_font, secord_title_font, first_title_size, secord_title_size

    def l_model(
            self,
            draw,
            config,
            first_title_location_x,
            first_title_location_y,
            component_location,
            secord_title_location_x,
            secord_title_location_y,
            first_title_font,
            secord_title_font,
            half_max_size,
            helf_height
    ):

        # 随机布局
        current_location = self.l_location()

        first_title_position_x = config["polarization"][current_location]["position"][0] - half_max_size + first_title_location_x
        first_title_position_y = config["polarization"][current_location]["position"][1] - helf_height + first_title_location_y
        secord_title_position_x = config["polarization"][current_location]["position"][0] - half_max_size + secord_title_location_x
        secord_title_position_y = config["polarization"][current_location]["position"][1] - helf_height + secord_title_location_y

        component_position = []

        for ikey in component_location:
            component_position_x = config["polarization"][current_location]["position"][0] - half_max_size + ikey[0]
            component_position_y = config["polarization"][current_location]["position"][1] - helf_height + ikey[1]
            component_position.append(
                [component_position_x, component_position_y, ikey[2]]
            )

        self.title_render(
            draw,
            config,
            component_position,
            first_title_position_x,
            first_title_position_y,
            secord_title_position_x,
            secord_title_position_y,
            first_title_font,
            secord_title_font
        )

    def x_model(self, config):

        # init
        draw, first_title_font, secord_title_font, first_title_size, secord_title_size = self.model_init(config)

        # 随机布局
        current_location = self.x_location()

        # 偏移值为正，上比下长；偏移值为负，下比上长；
        max_size = max(first_title_size[0], secord_title_size[0])

        # 下边这些全都是相对位置
        line_space = first_title_size[1] * config["other"]["space"]

        # 定左组件动右组件
        if config["polarization"][current_location]["option"] == 0:

            # 逐层往下确定绝对定位
            component_01_position_x = config["polarization"][current_location]["position"][0]
            component_01_position_y = config["polarization"][current_location]["position"][1]

            first_title_position_x = component_01_position_x + config["component"][0]["offset"][0]
            first_title_position_y = component_01_position_y + config["component"][0]["offset"][1]

            secord_title_position_x = component_01_position_x + config["component"][0]["offset"][0]
            secord_title_position_y = component_01_position_y + line_space + config["component"][0]["offset"][1]

            component_02_position_x = component_01_position_x + max_size + config["component"][1]["offset"][0] + config["component"][0]["offset"][0]
            component_02_position_y = component_01_position_y + line_space + config["component"][1]["offset"][1] + config["component"][0]["offset"][1]

            component_position = [
                [component_02_position_x, component_02_position_y, 1],
                [component_01_position_x, component_01_position_y, 0]
            ]

            self.title_render(
                draw,
                config,
                component_position,
                first_title_position_x,
                first_title_position_y,
                secord_title_position_x,
                secord_title_position_y,
                first_title_font,
                secord_title_font
            )

        # 定右组件动左组件
        elif config["polarization"][current_location]["option"] == 1:

            component_02 = Image.open("cover_generator/components/" + config["component"][1]["path"])

            component_02_position_x = config["polarization"][current_location]["position"][0] - component_02.width
            component_02_position_y = config["polarization"][current_location]["position"][1] - component_02.height

            secord_title_position_x = config["polarization"][current_location]["position"][0] - config["component"][1]["offset"][0] - secord_title_size[0] - component_02.width
            secord_title_position_y = config["polarization"][current_location]["position"][1] - config["component"][1]["offset"][1] - component_02.height

            first_title_position_x = config["polarization"][current_location]["position"][0] - config["component"][1]["offset"][0] - first_title_size[0] - component_02.width
            first_title_position_y = config["polarization"][current_location]["position"][1] - config["component"][1]["offset"][1] - line_space - component_02.height

            component_01_position_x = component_02_position_x - max_size - config["component"][0]["offset"][0]
            component_01_position_y = component_02_position_y - line_space - config["component"][0]["offset"][1]

            component_position = [
                [component_02_position_x, component_02_position_y, 1],
                [component_01_position_x, component_01_position_y, 0]
            ]

            self.title_render(
                draw,
                config,
                component_position,
                first_title_position_x,
                first_title_position_y,
                secord_title_position_x,
                secord_title_position_y,
                first_title_font,
                secord_title_font
            )

        # 定中央动左右
        else:

            first_title_position_x = config["polarization"][current_location]["position"][0] - first_title_size[0] / 2
            first_title_position_y = config["polarization"][current_location]["position"][1] - (first_title_size[1] + secord_title_size[1] + line_space) / 2

            secord_title_position_x = config["polarization"][current_location]["position"][0] - secord_title_size[0] / 2
            secord_title_position_y = first_title_position_y + line_space

            component_01_position_x = config["polarization"][current_location]["position"][0] - max_size / 2 - config["component"][0]["offset"][0]
            component_01_position_y = first_title_position_y - config["component"][0]["offset"][1]

            component_02_position_x = config["polarization"][current_location]["position"][0] + max_size / 2 + config["component"][1]["offset"][0]
            component_02_position_y = secord_title_position_y + config["component"][1]["offset"][1]

            component_position = [
                [component_02_position_x, component_02_position_y, 1],
                [component_01_position_x, component_01_position_y, 0]
            ]

            self.title_render(
                draw,
                config,
                component_position,
                first_title_position_x,
                first_title_position_y,
                secord_title_position_x,
                secord_title_position_y,
                first_title_font,
                secord_title_font
            )

    def title_render(
            self,
            draw,
            config,
            component_position,
            first_title_position_x,
            first_title_position_y,
            secord_title_position_x,
            secord_title_position_y,
            first_title_font,
            secord_title_font
    ):

        # 解析字体及阴影颜色
        first_title_color = tuple(eval(config["text"][0]["color"]))
        secord_title_color = tuple(eval(config["text"][1]["color"]))
        shadow = tuple(eval(config["other"]["shadow"]))

        # 加载组件
        for ikey in component_position:
            component_temp = Image.open("cover_generator/components/" + config["component"][ikey[2]]["path"])
            self.tb.paste(component_temp, (int(ikey[0]), int(ikey[1])))

        draw.text((first_title_position_x + config["other"]["shadow_offset_x"], first_title_position_y + config["other"]["shadow_offset_y"]), self.first_title, font=first_title_font, fill=shadow)
        draw.text((first_title_position_x, first_title_position_y), self.first_title, font=first_title_font, fill=first_title_color)
        draw.text((secord_title_position_x + config["other"]["shadow_offset_x"], secord_title_position_y + config["other"]["shadow_offset_y"]), self.secord_title, font=secord_title_font, fill=shadow)
        draw.text((secord_title_position_x, secord_title_position_y), self.secord_title, font=secord_title_font, fill=secord_title_color)

        self.tb.save('cover_generator/transparent_title.png', quality=100)

    def traditional(self):

        # init
        config = self.layout_config["model"]["traditional"]
        self.x_model(config)

    def simplicity(self):

        # init
        config = self.layout_config["model"]["simplicity"]
        self.x_model(config)

    def technology(self):

        # init
        config = self.layout_config["model"]["techbuddies"]
        self.x_model(config)

    def simplify(self):

        # init
        config = self.layout_config["model"]["simplify"]
        self.x_model(config)

    def humorous(self):

        # init
        config = self.layout_config["model"]["humorous"]
        draw, first_title_font, secord_title_font, first_title_size, secord_title_size = self.model_init(config)
        component = Image.open("cover_generator/components/" + config["component"][0]["path"])

        # 以最长组件来对齐
        max_size = max(first_title_size[0], secord_title_size[0], component.width)

        # 行间距
        line_space = first_title_size[1] * config["other"]["space"]

        first_title_location_x = max_size / 2 - first_title_size[0] / 2
        first_title_location_y = 0

        component_location_x = max_size / 2 - component.width / 2
        component_location_y = line_space

        secord_title_location_x = max_size / 2 - secord_title_size[0] / 2
        secord_title_location_y = component_location_y + component.height

        height = secord_title_location_y + secord_title_size[1]

        component_location = [
            [component_location_x, component_location_y, 0]
        ]

        self.l_model(draw, config, first_title_location_x, first_title_location_y, component_location, secord_title_location_x, secord_title_location_y, first_title_font, secord_title_font, max_size / 2, height / 2)

    def classical(self):

        # init
        config = self.layout_config["model"]["classical"]
        draw, first_title_font, secord_title_font, first_title_size, secord_title_size = self.model_init(config)
        component = Image.open("cover_generator/components/" + config["component"][0]["path"])

        component_01_location_x = 0
        component_01_location_y = 0

        component_02_location_x = config["component"][0]["location"][0]
        component_02_location_y = config["component"][0]["location"][1]

        first_title_location_x = config["component"][0]["offset"][0]
        first_title_location_y = config["component"][0]["offset"][1]

        secord_title_location_x = config["component"][0]["location"][0] + component.width - config["component"][1]["offset"][0] - secord_title_size[0]
        secord_title_location_y = config["component"][0]["location"][1] + component.height - config["component"][1]["offset"][1] - secord_title_size[1]

        component_location = [
            [component_01_location_x, component_01_location_y, 0],
            [component_02_location_x, component_02_location_y, 0]
        ]

        max_size = component_02_location_x + component.width
        height = component_02_location_y + component.height

        self.l_model(draw, config, first_title_location_x, first_title_location_y, component_location, secord_title_location_x, secord_title_location_y, first_title_font, secord_title_font, max_size / 2, height / 2)

    def vertical(self):

        # init
        config = self.layout_config["model"]["vertical"]
        draw, first_title_font, secord_title_font, first_title_size, secord_title_size = self.model_init(config)
        component = Image.open("cover_generator/components/" + config["component"][0]["path"])

        # 以最长组件来对齐
        max_size = max(first_title_size[0] + secord_title_size[0] + 50, component.width)

        component_location_x = 0
        component_location_y = 0

        first_title_location_x = component.width / 2 - config["component"][0]["offset"][0] - first_title_size[0]
        first_title_location_y = component.height / 2 - config["component"][0]["offset"][1] - first_title_size[1]

        secord_title_location_x = component.width / 2 + config["component"][1]["offset"][0]
        secord_title_location_y = component.height / 2 + config["component"][1]["offset"][1]

        height = component.height

        component_location = [
            [component_location_x, component_location_y, 0]
        ]

        self.l_model(draw, config, first_title_location_x, first_title_location_y, component_location, secord_title_location_x, secord_title_location_y, first_title_font, secord_title_font, max_size / 2, height / 2)

    def focus(self):

        # init
        config = self.layout_config["model"]["focus"]
        draw, first_title_font, secord_title_font, first_title_size, secord_title_size = self.model_init(config)
        component = Image.open("cover_generator/components/" + config["component"][0]["path"])

        # 行间距
        line_space = first_title_size[1] * config["other"]["space"]

        # 以最长组件来对齐
        secord_line_length = 2 * component.width + secord_title_size[0] + config["component"][0]["offset"][0] + config["component"][1]["offset"][0]
        max_size = max(secord_line_length, first_title_size[0])

        first_title_location_x = (max_size - first_title_size[0]) / 2
        first_title_location_y = 0

        component_01_location_x = (max_size - secord_line_length) / 2 + config["other"]["line_offset"]
        component_01_location_y = line_space

        secord_title_location_x = (max_size - secord_line_length) / 2 + component.width + config["component"][0]["offset"][0] + config["other"]["line_offset"]
        secord_title_location_y = line_space

        component_02_location_x = (max_size - secord_line_length) / 2 + component.width + config["component"][0]["offset"][0] + secord_title_size[0] + config["component"][1]["offset"][0] + config["other"]["line_offset"]
        component_02_location_y = line_space

        height = max(component.height, secord_title_size[1]) + line_space

        component_location = [
            [component_01_location_x, component_01_location_y, 0],
            [component_02_location_x, component_02_location_y, 0]
        ]

        self.l_model(draw, config, first_title_location_x, first_title_location_y, component_location, secord_title_location_x, secord_title_location_y, first_title_font, secord_title_font, max_size / 2, height / 2)

    def fresh(self):

        # init
        config = self.layout_config["model"]["fresh"]
        draw, first_title_font, secord_title_font, first_title_size, secord_title_size = self.model_init(config)
        component = Image.open("cover_generator/components/" + config["component"][0]["path"])

        # 行间距
        line_space = first_title_size[1] * config["other"]["space"]

        # 以最长组件来对齐
        first_line_length = 2 * component.width + first_title_size[0] + config["component"][0]["offset"][0] + config["component"][1]["offset"][0]
        max_size = max(first_line_length, secord_title_size[0])

        component_01_location_x = (max_size - first_line_length) / 2
        component_01_location_y = config["component"][0]["offset"][1]

        first_title_location_x = (max_size - first_line_length) / 2 + component.width + config["component"][0]["offset"][0]
        first_title_location_y = 0

        component_02_location_x = (max_size - first_line_length) / 2 + component.width + config["component"][0]["offset"][0] + first_title_size[0] + config["component"][1]["offset"][0]
        component_02_location_y = config["component"][1]["offset"][1]

        secord_title_location_x = (max_size - secord_title_size[0]) / 2 + config["other"]["line_offset"]
        secord_title_location_y = line_space

        height = secord_title_size[1] + line_space

        component_location = [
            [component_01_location_x, component_01_location_y, 0],
            [component_02_location_x, component_02_location_y, 0]
        ]

        self.l_model(draw, config, first_title_location_x, first_title_location_y, component_location, secord_title_location_x, secord_title_location_y, first_title_font, secord_title_font, max_size / 2, height / 2)

    # 返回模型
    def x_location(self):
        # 「4+1」模型：0居中 1左上 2右上 3右下 4左下
        # 随机一个位置
        location = random.randint(0, 4)
        return self.x_model_map[location]

    # 返回模型
    def l_location(self):
        # 「3中」模型：0中上 1中中 2中下
        # 随机一个位置
        location = random.randint(0, 2)
        return self.l_model_map[location]

    # 返回字体
    def random_font(self):
        font_list = []
        for root, dirs, files in os.walk(self.font_path):
            for file in files:
                if os.path.splitext(file)[-1] == '.ttf':
                    font_list.append(file)

        return random.choice(font_list)

    def run(self, first, secord):
        self.first_title = first
        self.secord_title = secord

        # 随机一个模型
        model = random.randint(0, 8)
        self.structure_map[model]()
