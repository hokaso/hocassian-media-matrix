import sys, os, time, json, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from cover_generator.typesetting.more import More
from cover_generator.typesetting.mark import Mark
from cover_generator.typesetting.build import Build
from utils.snow_id import SnowId

sys.path.append(os.getcwd())


class Four(object):

    def __init__(self, folder_key):

        self.image_list = None
        self.rank_model = None
        self.tb = None

        with open("cover_generator/typesetting/style.json", 'r') as f0:
            style_config = json.load(f0)

        self.model = style_config["four"]

        self.func_map = {
            1: self.quadruple_vertical_build,
            2: self.quadruple_horizontal_build,
            3: self.chairs_build,
            4: self.chairs_spin_build,
            5: self.h2v2_build,
            6: self.h2v2_spin_build,
            7: self.windows_build,
            8: self.windows_vertical_build,
            9: self.windows_horizontal_build,
        }

        self._build = Build(folder_key, folder_key + "_temp")

    def quadruple_vertical(self, image_list):
        return More(image_list, self.model[0]["unit_detail"], "41").main()

    def quadruple_horizontal(self, image_list):
        return More(image_list, self.model[1]["unit_detail"], "42").main()

    def chairs(self, image_list):
        return More(image_list, self.model[2]["unit_detail"], "43").main()

    def chairs_spin(self, image_list):
        return More(image_list, self.model[3]["unit_detail"], "44").main()

    def h2v2(self, image_list):
        return More(image_list, self.model[4]["unit_detail"], "45").main()

    def h2v2_spin(self, image_list):
        return More(image_list, self.model[5]["unit_detail"], "46").main()

    def windows(self, image_list):
        return More(image_list, self.model[6]["unit_detail"], "47").main()

    def windows_vertical(self, image_list):
        return More(image_list, self.model[7]["unit_detail"], "48").main()

    def windows_horizontal(self, image_list):
        return More(image_list, self.model[8]["unit_detail"], "49").main()

    def build(self, image_list, model):

        self.tb = Image.open("cover_generator/background.jpg")
        self.image_list = image_list
        self.rank_model = model
        self.func_map[int(model["model_id"][1])]()

    def quadruple_vertical_build(self):

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

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[0]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_1, pic_2, pic_3]
        random.shuffle(pic_list)

        # 结构也需要shuffle
        kind = random.randint(0, 1)

        # 保存
        if kind == 0:
            self.tb.paste(pic_list[0], (0, 0))
            self.tb.paste(pic_list[1], (0, 480))
            self.tb.paste(pic_list[2], (0, 960))
            self.tb.paste(pic_4, (540, 0))
        else:
            self.tb.paste(pic_list[0], (540, 0))
            self.tb.paste(pic_list[1], (540, 480))
            self.tb.paste(pic_list[2], (540, 960))
            self.tb.paste(pic_4, (0, 0))

        self._build.save(self.tb)

    def quadruple_horizontal_build(self):

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

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[1]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_1, pic_2, pic_3]
        random.shuffle(pic_list)

        # 结构也需要shuffle
        kind = random.randint(0, 1)

        # {
        #     "width": 360,
        #     "height": 720
        # },
        # {
        #     "width": 360,
        #     "height": 720
        # },
        # {
        #     "width": 360,
        #     "height": 720
        # },
        # {
        #     "width": 1080,
        #     "height": 720
        # }

        # 保存
        if kind == 0:
            self.tb.paste(pic_list[0], (0, 0))
            self.tb.paste(pic_list[1], (360, 0))
            self.tb.paste(pic_list[2], (720, 0))
            self.tb.paste(pic_4, (0, 720))
        else:
            self.tb.paste(pic_list[0], (0, 720))
            self.tb.paste(pic_list[1], (360, 720))
            self.tb.paste(pic_list[2], (720, 720))
            self.tb.paste(pic_4, (0, 0))

        self._build.save(self.tb)

    def chairs_build(self):

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

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[2]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_2, pic_3]
        random.shuffle(pic_list)

        # 结构也需要shuffle
        kind = random.randint(0, 3)

        # {
        #     "width": 720,
        #     "height": 720
        # },
        # {
        #     "width": 360,
        #     "height": 720
        # },
        # {
        #     "width": 360,
        #     "height": 720
        # },
        # {
        #     "width": 360,
        #     "height": 1440
        # }

        # 保存
        if kind == 0:
            self.tb.paste(pic_1, (0, 0))
            self.tb.paste(pic_list[1], (0, 720))
            self.tb.paste(pic_list[0], (360, 720))
            self.tb.paste(pic_4, (720, 0))
        elif kind == 1:
            self.tb.paste(pic_1, (360, 0))
            self.tb.paste(pic_list[1], (360, 720))
            self.tb.paste(pic_list[0], (720, 720))
            self.tb.paste(pic_4, (0, 0))
        elif kind == 2:
            self.tb.paste(pic_1, (0, 720))
            self.tb.paste(pic_list[1], (0, 0))
            self.tb.paste(pic_list[0], (360, 0))
            self.tb.paste(pic_4, (720, 0))
        else:
            self.tb.paste(pic_1, (360, 720))
            self.tb.paste(pic_list[1], (360, 0))
            self.tb.paste(pic_list[0], (720, 0))
            self.tb.paste(pic_4, (0, 0))

        self._build.save(self.tb)

    def chairs_spin_build(self):

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

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[3]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_3, pic_4]
        random.shuffle(pic_list)

        # 结构也需要shuffle
        kind = random.randint(0, 3)

        # 保存

        # {
        #     "width": 1080,
        #     "height": 480
        # },
        # {
        #     "width": 540,
        #     "height": 960
        # },
        # {
        #     "width": 540,
        #     "height": 480
        # },
        # {
        #     "width": 540,
        #     "height": 480
        # }

        if kind == 0:
            self.tb.paste(pic_1, (0, 0))
            self.tb.paste(pic_2, (0, 480))
            self.tb.paste(pic_list[1], (540, 480))
            self.tb.paste(pic_list[0], (540, 960))
        elif kind == 1:
            self.tb.paste(pic_1, (0, 0))
            self.tb.paste(pic_2, (540, 480))
            self.tb.paste(pic_list[1], (0, 480))
            self.tb.paste(pic_list[0], (0, 960))
        elif kind == 2:
            self.tb.paste(pic_1, (0, 960))
            self.tb.paste(pic_2, (0, 0))
            self.tb.paste(pic_list[1], (540, 0))
            self.tb.paste(pic_list[0], (540, 480))
        else:
            self.tb.paste(pic_1, (0, 960))
            self.tb.paste(pic_2, (540, 0))
            self.tb.paste(pic_list[1], (0, 480))
            self.tb.paste(pic_list[0], (0, 0))

        self._build.save(self.tb)

    def h2v2_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[4]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = self._build.build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[4]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = self._build.build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[4]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = self._build.build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[4]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_3, pic_4]
        random.shuffle(pic_list_2)

        # 结构也需要shuffle，此处三种结构
        kind = random.randint(0, 2)

        # 保存
        if kind == 0:
            self.tb.paste(pic_list_1[0], (0, 0))
            self.tb.paste(pic_list_1[1], (0, 720))
            self.tb.paste(pic_list_2[0], (360, 0))
            self.tb.paste(pic_list_2[1], (720, 0))
        elif kind == 1:
            self.tb.paste(pic_list_1[0], (720, 0))
            self.tb.paste(pic_list_1[1], (720, 720))
            self.tb.paste(pic_list_2[0], (0, 0))
            self.tb.paste(pic_list_2[1], (360, 0))
        else:
            self.tb.paste(pic_list_1[0], (360, 0))
            self.tb.paste(pic_list_1[1], (360, 720))
            self.tb.paste(pic_list_2[0], (0, 0))
            self.tb.paste(pic_list_2[1], (720, 0))

        self._build.save(self.tb)

    def h2v2_spin_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[5]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = self._build.build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[5]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = self._build.build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[5]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = self._build.build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[5]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_3, pic_4]
        random.shuffle(pic_list_2)

        # 结构也需要shuffle，此处三种结构
        kind = random.randint(0, 2)

        # 保存

        # {
        #     "width": 1080,
        #     "height": 480
        # },
        # {
        #     "width": 1080,
        #     "height": 480
        # },
        # {
        #     "width": 540,
        #     "height": 480
        # },
        # {
        #     "width": 540,
        #     "height": 480
        # }

        if kind == 0:
            self.tb.paste(pic_list_1[0], (0, 0))
            self.tb.paste(pic_list_1[1], (0, 480))
            self.tb.paste(pic_list_2[0], (0, 960))
            self.tb.paste(pic_list_2[1], (540, 960))
        elif kind == 1:
            self.tb.paste(pic_list_1[0], (0, 480))
            self.tb.paste(pic_list_1[1], (0, 960))
            self.tb.paste(pic_list_2[0], (0, 0))
            self.tb.paste(pic_list_2[1], (540, 0))
        else:
            self.tb.paste(pic_list_1[0], (0, 0))
            self.tb.paste(pic_list_1[1], (0, 960))
            self.tb.paste(pic_list_2[0], (0, 480))
            self.tb.paste(pic_list_2[1], (540, 480))

        self._build.save(self.tb)

    def windows_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[6]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = self._build.build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[6]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = self._build.build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[6]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = self._build.build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[6]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_1, pic_2, pic_3, pic_4]
        random.shuffle(pic_list)

        self.tb.paste(pic_list[0], (0, 0))
        self.tb.paste(pic_list[1], (540, 0))
        self.tb.paste(pic_list[2], (0, 720))
        self.tb.paste(pic_list[3], (540, 720))

        self._build.save(self.tb)

    def windows_vertical_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[7]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = self._build.build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[7]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = self._build.build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[7]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = self._build.build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[7]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_3, pic_4]
        random.shuffle(pic_list_2)

        # 结构也需要shuffle，此处2种结构
        kind = random.randint(0, 1)

        # 保存
        if kind == 0:
            self.tb.paste(pic_list_1[0], (0, 0))
            self.tb.paste(pic_list_1[1], (360, 720))
            self.tb.paste(pic_list_2[0], (720, 0))
            self.tb.paste(pic_list_2[1], (0, 720))
        else:
            self.tb.paste(pic_list_1[0], (360, 0))
            self.tb.paste(pic_list_1[1], (0, 720))
            self.tb.paste(pic_list_2[0], (0, 0))
            self.tb.paste(pic_list_2[1], (720, 720))

        self._build.save(self.tb)

    def windows_horizontal_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[8]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = self._build.build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[8]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = self._build.build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[8]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = self._build.build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[8]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = self._build.build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_3, pic_4]
        random.shuffle(pic_list_2)

        # 结构也需要shuffle，此处2种结构
        kind = random.randint(0, 1)

        # 保存
        if kind == 0:
            self.tb.paste(pic_list_1[0], (0, 0))
            self.tb.paste(pic_list_1[1], (540, 1080))
            self.tb.paste(pic_list_2[0], (540, 0))
            self.tb.paste(pic_list_2[1], (0, 360))
        else:
            self.tb.paste(pic_list_1[0], (540, 0))
            self.tb.paste(pic_list_1[1], (0, 1080))
            self.tb.paste(pic_list_2[0], (0, 0))
            self.tb.paste(pic_list_2[1], (540, 360))

        self._build.save(self.tb)
