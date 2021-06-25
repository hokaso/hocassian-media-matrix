import sys, os, time, json, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from cover_generator.typesetting.more import More
from cover_generator.typesetting.mark import Mark
from cover_generator.typesetting.build import Build
from utils.snow_id import SnowId

sys.path.append(os.getcwd())


class Three(object):

    def __init__(self, folder_key):

        self.image_list = None
        self.rank_model = None
        self.tb = None

        with open("cover_generator/typesetting/style.json", 'r') as f0:
            style_config = json.loads(f0.read())

        self.model = style_config["three"]

        self.func_map = {
            1: self.horizontal_build,
            2: self.vertical_build,
            3: self.triple_vertical_build,
            4: self.triple_horizontal_build
        }

        self._build = Build(folder_key, folder_key + "_temp")

    def horizontal(self, image_list):

        return More(image_list, self.model[0]["unit_detail"], "31").main()

    def vertical(self, image_list):

        return More(image_list, self.model[1]["unit_detail"], "32").main()

    def triple_vertical(self, image_list):

        return More(image_list, self.model[2]["unit_detail"], "33").main()

    def triple_horizontal(self, image_list):

        return More(image_list, self.model[3]["unit_detail"], "34").main()

    def build(self, image_list, model):

        self.tb = Image.open("cover_generator/background.jpg")
        self.image_list = image_list
        self.rank_model = model
        self.func_map[int(model["model_id"][1])]()

    def horizontal_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[0]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = self._build.build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[0]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = self._build.build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[0]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_1, pic_2, pic_3]
        random.shuffle(pic_list)

        # 保存
        self.tb.paste(pic_list[0], (0, 0))
        self.tb.paste(pic_list[1], (0, 480))
        self.tb.paste(pic_list[2], (0, 960))
        self._build.save(self.tb)

    def vertical_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[1]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = self._build.build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[1]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = self._build.build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[1]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_1, pic_2, pic_3]
        random.shuffle(pic_list)

        # 保存
        self.tb.paste(pic_list[0], (0, 0))
        self.tb.paste(pic_list[1], (360, 0))
        self.tb.paste(pic_list[2], (720, 0))
        self._build.save(self.tb)

    def triple_vertical_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[2]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = self._build.build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[2]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = self._build.build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[2]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_1, pic_2]
        random.shuffle(pic_list)

        # 结构也需要shuffle
        kind = random.randint(0, 1)

        # 保存
        if kind == 0:
            self.tb.paste(pic_list[0], (0, 0))
            self.tb.paste(pic_list[1], (0, 720))
            self.tb.paste(pic_3, (540, 0))
        else:
            self.tb.paste(pic_list[0], (540, 0))
            self.tb.paste(pic_list[1], (540, 720))
            self.tb.paste(pic_3, (0, 0))

        self._build.save(self.tb)

    def triple_horizontal_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[3]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = self._build.build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[3]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = self._build.build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[3]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_1, pic_2]
        random.shuffle(pic_list)

        # 结构也需要shuffle
        kind = random.randint(0, 1)

        # 保存
        if kind == 0:
            self.tb.paste(pic_list[0], (0, 0))
            self.tb.paste(pic_list[1], (540, 0))
            self.tb.paste(pic_3, (0, 720))
        else:
            self.tb.paste(pic_list[0], (0, 720))
            self.tb.paste(pic_list[1], (540, 720))
            self.tb.paste(pic_3, (0, 0))

        self._build.save(self.tb)
