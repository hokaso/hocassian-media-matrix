import sys, os, time, json, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from cover_generator.typesetting.more import More
from cover_generator.typesetting.mark import Mark
from cover_generator.typesetting.build import Build
from utils.snow_id import SnowId

sys.path.append(os.getcwd())


class Six(object):

    def __init__(self):

        self.image_list = None
        self.rank_model = None
        self.tb = None

        with open("cover_generator/typesetting/style.json", 'r') as f0:
            style_config = json.loads(f0.read())

        self.model = style_config["six"]

        self.func_map = {
            1: self.align_vertical_build,
            2: self.align_horizontal_build,
            3: self.offset_vertical_small_build,
            4: self.offset_horizontal_small_build,
            5: self.offset_vertical_big_build,
            6: self.offset_horizontal_big_build,
            7: self.arround_build,
        }

    def align_vertical(self, image_list):
        return More(image_list, self.model[0]["unit_detail"], "61").main()

    def align_horizontal(self, image_list):
        return More(image_list, self.model[1]["unit_detail"], "62").main()

    def offset_vertical_small(self, image_list):
        return More(image_list, self.model[2]["unit_detail"], "63").main()

    def offset_horizontal_small(self, image_list):
        return More(image_list, self.model[3]["unit_detail"], "64").main()

    def offset_vertical_big(self, image_list):
        return More(image_list, self.model[4]["unit_detail"], "65").main()

    def offset_horizontal_big(self, image_list):
        return More(image_list, self.model[4]["unit_detail"], "66").main()

    def arround(self, image_list):
        return More(image_list, self.model[4]["unit_detail"], "67").main()

    def build(self, image_list, model):

        self.tb = Image.open("background.jpg")
        self.image_list = image_list
        self.rank_model = model
        self.func_map[int(model["model_id"][1])]()

    def align_vertical_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[0]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = Build().build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[0]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = Build().build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[0]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = Build().build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[0]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = Build().build_up(image["filename"], rate, area)

        # 贴第五张图
        image = self.image_list[self.rank_model["model_match"][4][1]]
        model = self.model[0]["unit_detail"][4]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_5 = Build().build_up(image["filename"], rate, area)

        # 贴第六张图
        image = self.image_list[self.rank_model["model_match"][5][1]]
        model = self.model[0]["unit_detail"][5]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_6 = Build().build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_1, pic_2, pic_3, pic_4, pic_5, pic_6]
        random.shuffle(pic_list)

        self.tb.paste(pic_list[0], (0, 0))
        self.tb.paste(pic_list[1], (360, 0))
        self.tb.paste(pic_list[2], (720, 0))
        self.tb.paste(pic_list[3], (0, 720))
        self.tb.paste(pic_list[4], (360, 720))
        self.tb.paste(pic_list[5], (720, 720))

        Build().save(self.tb)

    def align_horizontal_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[1]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = Build().build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[1]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = Build().build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[1]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = Build().build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[1]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = Build().build_up(image["filename"], rate, area)

        # 贴第五张图
        image = self.image_list[self.rank_model["model_match"][4][1]]
        model = self.model[1]["unit_detail"][4]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_5 = Build().build_up(image["filename"], rate, area)

        # 贴第六张图
        image = self.image_list[self.rank_model["model_match"][5][1]]
        model = self.model[1]["unit_detail"][5]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_6 = Build().build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_1, pic_2, pic_3, pic_4, pic_5, pic_6]
        random.shuffle(pic_list)

        self.tb.paste(pic_list[0], (0, 0))
        self.tb.paste(pic_list[1], (540, 0))
        self.tb.paste(pic_list[2], (0, 480))
        self.tb.paste(pic_list[3], (540, 480))
        self.tb.paste(pic_list[4], (0, 960))
        self.tb.paste(pic_list[5], (540, 960))

        Build().save(self.tb)

    def offset_vertical_small_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[2]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = Build().build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[2]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = Build().build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[2]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = Build().build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[2]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = Build().build_up(image["filename"], rate, area)

        # 贴第五张图
        image = self.image_list[self.rank_model["model_match"][4][1]]
        model = self.model[2]["unit_detail"][4]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_5 = Build().build_up(image["filename"], rate, area)

        # 贴第六张图
        image = self.image_list[self.rank_model["model_match"][5][1]]
        model = self.model[2]["unit_detail"][5]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_6 = Build().build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_3, pic_4]
        random.shuffle(pic_list_2)

        pic_list_3 = [pic_5, pic_6]
        random.shuffle(pic_list_3)

        # 结构也需要shuffle，此处6种结构
        kind_1 = random.randint(0, 1)
        kind_2 = random.randint(0, 2)

        # 保存
        if kind_1 == 0:
            if kind_2 == 0:
                self.tb.paste(pic_list_1[0], (0, 0))
                self.tb.paste(pic_list_1[1], (0, 360))
                self.tb.paste(pic_list_2[0], (360, 0))
                self.tb.paste(pic_list_2[1], (720, 0))
                self.tb.paste(pic_list_3[0], (0, 720))
                self.tb.paste(pic_list_3[1], (540, 720))
            elif kind_2 == 1:
                self.tb.paste(pic_list_1[0], (360, 0))
                self.tb.paste(pic_list_1[1], (360, 360))
                self.tb.paste(pic_list_2[0], (0, 0))
                self.tb.paste(pic_list_2[1], (720, 0))
                self.tb.paste(pic_list_3[0], (0, 720))
                self.tb.paste(pic_list_3[1], (540, 720))
            else:
                self.tb.paste(pic_list_1[0], (720, 0))
                self.tb.paste(pic_list_1[1], (720, 360))
                self.tb.paste(pic_list_2[0], (0, 0))
                self.tb.paste(pic_list_2[1], (360, 0))
                self.tb.paste(pic_list_3[0], (0, 720))
                self.tb.paste(pic_list_3[1], (540, 720))

        else:
            if kind_2 == 0:
                self.tb.paste(pic_list_1[0], (0, 720))
                self.tb.paste(pic_list_1[1], (0, 1080))
                self.tb.paste(pic_list_2[0], (360, 720))
                self.tb.paste(pic_list_2[1], (720, 720))
                self.tb.paste(pic_list_3[0], (0, 0))
                self.tb.paste(pic_list_3[1], (540, 0))
            elif kind_2 == 1:
                self.tb.paste(pic_list_1[0], (360, 720))
                self.tb.paste(pic_list_1[1], (360, 1080))
                self.tb.paste(pic_list_2[0], (0, 720))
                self.tb.paste(pic_list_2[1], (720, 720))
                self.tb.paste(pic_list_3[0], (0, 0))
                self.tb.paste(pic_list_3[1], (540, 0))
            else:
                self.tb.paste(pic_list_1[0], (720, 720))
                self.tb.paste(pic_list_1[1], (720, 1080))
                self.tb.paste(pic_list_2[0], (0, 720))
                self.tb.paste(pic_list_2[1], (360, 720))
                self.tb.paste(pic_list_3[0], (0, 0))
                self.tb.paste(pic_list_3[1], (540, 0))

        Build().save(self.tb)

    def offset_horizontal_small_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[3]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = Build().build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[3]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = Build().build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[3]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = Build().build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[3]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = Build().build_up(image["filename"], rate, area)

        # 贴第五张图
        image = self.image_list[self.rank_model["model_match"][4][1]]
        model = self.model[3]["unit_detail"][4]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_5 = Build().build_up(image["filename"], rate, area)

        # 贴第六张图
        image = self.image_list[self.rank_model["model_match"][5][1]]
        model = self.model[3]["unit_detail"][5]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_6 = Build().build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_3, pic_4]
        random.shuffle(pic_list_2)

        pic_list_3 = [pic_5, pic_6]
        random.shuffle(pic_list_3)

        # 结构也需要shuffle，此处6种结构
        kind_1 = random.randint(0, 1)
        kind_2 = random.randint(0, 2)

        # 保存
        if kind_1 == 0:
            if kind_2 == 0:
                self.tb.paste(pic_list_1[0], (0, 0))
                self.tb.paste(pic_list_1[1], (270, 0))
                self.tb.paste(pic_list_2[0], (0, 480))
                self.tb.paste(pic_list_2[1], (0, 960))
                self.tb.paste(pic_list_3[0], (540, 0))
                self.tb.paste(pic_list_3[1], (540, 720))
            elif kind_2 == 1:
                self.tb.paste(pic_list_1[0], (0, 480))
                self.tb.paste(pic_list_1[1], (270, 480))
                self.tb.paste(pic_list_2[0], (0, 0))
                self.tb.paste(pic_list_2[1], (0, 960))
                self.tb.paste(pic_list_3[0], (540, 0))
                self.tb.paste(pic_list_3[1], (540, 720))
            else:
                self.tb.paste(pic_list_1[0], (0, 960))
                self.tb.paste(pic_list_1[1], (270, 960))
                self.tb.paste(pic_list_2[0], (0, 480))
                self.tb.paste(pic_list_2[1], (0, 0))
                self.tb.paste(pic_list_3[0], (540, 0))
                self.tb.paste(pic_list_3[1], (540, 720))

        else:
            if kind_2 == 0:
                self.tb.paste(pic_list_1[0], (540, 0))
                self.tb.paste(pic_list_1[1], (810, 0))
                self.tb.paste(pic_list_2[0], (540, 480))
                self.tb.paste(pic_list_2[1], (540, 960))
                self.tb.paste(pic_list_3[0], (0, 0))
                self.tb.paste(pic_list_3[1], (0, 720))
            elif kind_2 == 1:
                self.tb.paste(pic_list_1[0], (540, 480))
                self.tb.paste(pic_list_1[1], (810, 480))
                self.tb.paste(pic_list_2[0], (540, 0))
                self.tb.paste(pic_list_2[1], (540, 960))
                self.tb.paste(pic_list_3[0], (0, 0))
                self.tb.paste(pic_list_3[1], (0, 720))
            else:
                self.tb.paste(pic_list_1[0], (540, 960))
                self.tb.paste(pic_list_1[1], (810, 960))
                self.tb.paste(pic_list_2[0], (540, 480))
                self.tb.paste(pic_list_2[1], (540, 0))
                self.tb.paste(pic_list_3[0], (0, 0))
                self.tb.paste(pic_list_3[1], (0, 720))

        Build().save(self.tb)

    def offset_vertical_big_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[4]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = Build().build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[4]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = Build().build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[4]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = Build().build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[4]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = Build().build_up(image["filename"], rate, area)

        # 贴第五张图
        image = self.image_list[self.rank_model["model_match"][4][1]]
        model = self.model[4]["unit_detail"][4]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_5 = Build().build_up(image["filename"], rate, area)

        # 贴第六张图
        image = self.image_list[self.rank_model["model_match"][5][1]]
        model = self.model[4]["unit_detail"][5]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_6 = Build().build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2, pic_3]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_4, pic_5]
        random.shuffle(pic_list_2)

        # 结构也需要shuffle，此处4种结构
        kind_1 = random.randint(0, 1)
        kind_2 = random.randint(0, 1)

        # 保存
        if kind_1 == 0:
            if kind_2 == 0:
                self.tb.paste(pic_list_1[0], (0, 0))
                self.tb.paste(pic_list_1[1], (360, 0))
                self.tb.paste(pic_list_1[2], (720, 0))
                self.tb.paste(pic_list_2[1], (540, 720))
                self.tb.paste(pic_list_2[0], (540, 1080))
                self.tb.paste(pic_6, (0, 720))
            else:
                self.tb.paste(pic_list_1[0], (0, 0))
                self.tb.paste(pic_list_1[1], (360, 0))
                self.tb.paste(pic_list_1[2], (720, 0))
                self.tb.paste(pic_list_2[1], (0, 720))
                self.tb.paste(pic_list_2[0], (0, 1080))
                self.tb.paste(pic_6, (540, 720))

        else:
            if kind_2 == 0:
                self.tb.paste(pic_list_1[0], (0, 720))
                self.tb.paste(pic_list_1[1], (360, 720))
                self.tb.paste(pic_list_1[2], (720, 720))
                self.tb.paste(pic_list_2[1], (0, 0))
                self.tb.paste(pic_list_2[0], (0, 360))
                self.tb.paste(pic_6, (540, 0))
            else:
                self.tb.paste(pic_list_1[0], (0, 720))
                self.tb.paste(pic_list_1[1], (360, 720))
                self.tb.paste(pic_list_1[2], (720, 720))
                self.tb.paste(pic_list_2[1], (540, 0))
                self.tb.paste(pic_list_2[0], (540, 360))
                self.tb.paste(pic_6, (0, 0))

        Build().save(self.tb)

    def offset_horizontal_big_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[5]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = Build().build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[5]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = Build().build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[5]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = Build().build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[5]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = Build().build_up(image["filename"], rate, area)

        # 贴第五张图
        image = self.image_list[self.rank_model["model_match"][4][1]]
        model = self.model[5]["unit_detail"][4]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_5 = Build().build_up(image["filename"], rate, area)

        # 贴第六张图
        image = self.image_list[self.rank_model["model_match"][5][1]]
        model = self.model[5]["unit_detail"][5]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_6 = Build().build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2, pic_3]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_4, pic_5]
        random.shuffle(pic_list_2)

        # 结构也需要shuffle，此处4种结构
        kind_1 = random.randint(0, 1)
        kind_2 = random.randint(0, 1)

        # 保存
        if kind_1 == 0:
            if kind_2 == 0:
                self.tb.paste(pic_list_1[0], (0, 0))
                self.tb.paste(pic_list_1[1], (0, 480))
                self.tb.paste(pic_list_1[2], (0, 960))
                self.tb.paste(pic_list_2[1], (540, 0))
                self.tb.paste(pic_list_2[0], (810, 0))
                self.tb.paste(pic_6, (540, 720))
            else:
                self.tb.paste(pic_list_1[0], (0, 0))
                self.tb.paste(pic_list_1[1], (0, 480))
                self.tb.paste(pic_list_1[2], (0, 960))
                self.tb.paste(pic_list_2[1], (540, 720))
                self.tb.paste(pic_list_2[0], (810, 720))
                self.tb.paste(pic_6, (540, 0))

        else:
            if kind_2 == 0:
                self.tb.paste(pic_list_1[0], (540, 0))
                self.tb.paste(pic_list_1[1], (540, 480))
                self.tb.paste(pic_list_1[2], (540, 960))
                self.tb.paste(pic_list_2[1], (0, 0))
                self.tb.paste(pic_list_2[0], (270, 0))
                self.tb.paste(pic_6, (0, 720))
            else:
                self.tb.paste(pic_list_1[0], (540, 0))
                self.tb.paste(pic_list_1[1], (540, 480))
                self.tb.paste(pic_list_1[2], (540, 960))
                self.tb.paste(pic_list_2[1], (0, 720))
                self.tb.paste(pic_list_2[0], (270, 720))
                self.tb.paste(pic_6, (0, 0))

        Build().save(self.tb)

    def arround_build(self):

        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[6]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_1 = Build().build_up(image["filename"], rate, area)

        # 贴第二张图
        image = self.image_list[self.rank_model["model_match"][1][1]]
        model = self.model[6]["unit_detail"][1]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_2 = Build().build_up(image["filename"], rate, area)

        # 贴第三张图
        image = self.image_list[self.rank_model["model_match"][2][1]]
        model = self.model[6]["unit_detail"][2]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_3 = Build().build_up(image["filename"], rate, area)

        # 贴第四张图
        image = self.image_list[self.rank_model["model_match"][3][1]]
        model = self.model[6]["unit_detail"][3]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_4 = Build().build_up(image["filename"], rate, area)

        # 贴第五张图
        image = self.image_list[self.rank_model["model_match"][4][1]]
        model = self.model[6]["unit_detail"][4]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_5 = Build().build_up(image["filename"], rate, area)

        # 贴第六张图
        image = self.image_list[self.rank_model["model_match"][5][1]]
        model = self.model[6]["unit_detail"][5]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic_6 = Build().build_up(image["filename"], rate, area)

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_1, pic_2, pic_3, pic_4, pic_5]
        random.shuffle(pic_list)

        # 结构也需要shuffle，此处4种结构
        kind_1 = random.randint(0, 1)
        kind_2 = random.randint(0, 1)

        # 保存
        if kind_1 == 0:
            if kind_2 == 0:
                self.tb.paste(pic_list[0], (0, 0))
                self.tb.paste(pic_list[1], (0, 480))
                self.tb.paste(pic_list[2], (0, 960))
                self.tb.paste(pic_list[3], (360, 0))
                self.tb.paste(pic_list[4], (720, 0))
                self.tb.paste(pic_6, (360, 480))
            else:
                self.tb.paste(pic_list[0], (0, 0))
                self.tb.paste(pic_list[1], (0, 480))
                self.tb.paste(pic_list[2], (0, 960))
                self.tb.paste(pic_list[3], (360, 960))
                self.tb.paste(pic_list[4], (720, 960))
                self.tb.paste(pic_6, (360, 0))

        else:
            if kind_2 == 0:
                self.tb.paste(pic_list[0], (720, 0))
                self.tb.paste(pic_list[1], (720, 480))
                self.tb.paste(pic_list[2], (720, 960))
                self.tb.paste(pic_list[3], (360, 960))
                self.tb.paste(pic_list[4], (0, 960))
                self.tb.paste(pic_6, (0, 0))
            else:
                self.tb.paste(pic_list[0], (720, 0))
                self.tb.paste(pic_list[1], (720, 480))
                self.tb.paste(pic_list[2], (720, 960))
                self.tb.paste(pic_list[3], (360, 0))
                self.tb.paste(pic_list[4], (0, 0))
                self.tb.paste(pic_6, (0, 480))

        Build().save(self.tb)
