import sys, os, time, json, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from cover_generator.typesetting.more import More
from cover_generator.typesetting.mark import Mark
from cover_generator.typesetting.build import Build
from utils.snow_id import SnowId

sys.path.append(os.getcwd())


class Five(object):

    def __init__(self):

        self.image_list = None
        self.rank_model = None
        self.tb = None

        with open("cover_generator/typesetting/style.json", 'r') as f0:
            style_config = json.loads(f0.read())

        self.model = style_config["five"]

        self.func_map = {
            1: self.offset_vertical_build,
            2: self.offset_horizontal_build,
            3: self.align_vertical_build,
            4: self.align_horizontal_build,
            5: self.mirror_build,
        }

    def offset_vertical(self, image_list):
        return More(image_list, self.model[0]["unit_detail"], "51").main()

    def offset_horizontal(self, image_list):
        return More(image_list, self.model[1]["unit_detail"], "52").main()

    def align_vertical(self, image_list):
        return More(image_list, self.model[2]["unit_detail"], "53").main()

    def align_horizontal(self, image_list):
        return More(image_list, self.model[3]["unit_detail"], "54").main()

    def mirror(self, image_list):
        return More(image_list, self.model[4]["unit_detail"], "55").main()

    def build(self, image_list, model):

        self.tb = Image.open("cover_generator/background.jpg")
        self.image_list = image_list
        self.rank_model = model
        self.func_map[int(model["model_id"][1])]()

    def offset_vertical_build(self):

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

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_3, pic_4, pic_5]
        random.shuffle(pic_list_2)

        # 结构也需要shuffle
        kind = random.randint(0, 1)

        # 保存
        if kind == 0:
            self.tb.paste(pic_list_1[0], (0, 0))
            self.tb.paste(pic_list_1[1], (0, 720))
            self.tb.paste(pic_list_2[0], (540, 0))
            self.tb.paste(pic_list_2[1], (540, 480))
            self.tb.paste(pic_list_2[2], (540, 960))
        else:
            self.tb.paste(pic_list_1[0], (540, 0))
            self.tb.paste(pic_list_1[1], (540, 720))
            self.tb.paste(pic_list_2[0], (0, 0))
            self.tb.paste(pic_list_2[1], (0, 480))
            self.tb.paste(pic_list_2[2], (0, 960))

        Build().save(self.tb)

    def offset_horizontal_build(self):

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

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_3, pic_4, pic_5]
        random.shuffle(pic_list_2)

        # 结构也需要shuffle
        kind = random.randint(0, 1)

        # 保存
        if kind == 0:
            self.tb.paste(pic_list_1[0], (0, 0))
            self.tb.paste(pic_list_1[1], (540, 0))
            self.tb.paste(pic_list_2[0], (0, 720))
            self.tb.paste(pic_list_2[1], (360, 720))
            self.tb.paste(pic_list_2[2], (720, 720))
        else:
            self.tb.paste(pic_list_1[0], (0, 720))
            self.tb.paste(pic_list_1[1], (540, 720))
            self.tb.paste(pic_list_2[0], (0, 0))
            self.tb.paste(pic_list_2[1], (360, 0))
            self.tb.paste(pic_list_2[2], (720, 0))

        Build().save(self.tb)

    def align_vertical_build(self):

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

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_2, pic_3, pic_4, pic_5]
        random.shuffle(pic_list)

        # 结构也需要shuffle
        kind = random.randint(0, 2)

        # 保存
        if kind == 0:
            self.tb.paste(pic_1, (0, 0))
            self.tb.paste(pic_list[0], (360, 0))
            self.tb.paste(pic_list[1], (360, 720))
            self.tb.paste(pic_list[2], (720, 0))
            self.tb.paste(pic_list[3], (720, 720))
        elif kind == 1:
            self.tb.paste(pic_1, (360, 0))
            self.tb.paste(pic_list[0], (0, 0))
            self.tb.paste(pic_list[1], (0, 720))
            self.tb.paste(pic_list[2], (720, 0))
            self.tb.paste(pic_list[3], (720, 720))
        else:
            self.tb.paste(pic_1, (720, 0))
            self.tb.paste(pic_list[0], (0, 0))
            self.tb.paste(pic_list[1], (0, 720))
            self.tb.paste(pic_list[2], (360, 0))
            self.tb.paste(pic_list[3], (360, 720))

        Build().save(self.tb)

    def align_horizontal_build(self):

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

        # 随机对相同宽高的图片进行shuffle
        pic_list = [pic_2, pic_3, pic_4, pic_5]
        random.shuffle(pic_list)

        # 结构也需要shuffle
        kind = random.randint(0, 2)

        # 保存
        if kind == 0:
            self.tb.paste(pic_1, (0, 0))
            self.tb.paste(pic_list[0], (0, 480))
            self.tb.paste(pic_list[1], (0, 960))
            self.tb.paste(pic_list[2], (540, 480))
            self.tb.paste(pic_list[3], (540, 960))
        elif kind == 1:
            self.tb.paste(pic_1, (0, 480))
            self.tb.paste(pic_list[0], (0, 0))
            self.tb.paste(pic_list[1], (540, 0))
            self.tb.paste(pic_list[2], (0, 960))
            self.tb.paste(pic_list[3], (540, 960))
        else:
            self.tb.paste(pic_1, (0, 960))
            self.tb.paste(pic_list[0], (0, 0))
            self.tb.paste(pic_list[1], (540, 0))
            self.tb.paste(pic_list[2], (0, 480))
            self.tb.paste(pic_list[3], (540, 480))

        Build().save(self.tb)

    def mirror_build(self):

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

        # 随机对相同宽高的图片进行shuffle
        pic_list_1 = [pic_1, pic_2]
        random.shuffle(pic_list_1)

        pic_list_2 = [pic_3, pic_4]
        random.shuffle(pic_list_2)

        # 结构也需要shuffle
        kind = random.randint(0, 1)

        # 保存
        if kind == 0:
            self.tb.paste(pic_list_1[0], (0, 0))
            self.tb.paste(pic_list_1[1], (360, 1080))
            self.tb.paste(pic_list_2[0], (0, 360))
            self.tb.paste(pic_list_2[1], (720, 0))
            self.tb.paste(pic_5, (360, 360))
        else:
            self.tb.paste(pic_list_1[0], (360, 0))
            self.tb.paste(pic_list_1[1], (0, 1080))
            self.tb.paste(pic_list_2[0], (0, 0))
            self.tb.paste(pic_list_2[1], (720, 360))
            self.tb.paste(pic_5, (360, 360))

        Build().save(self.tb)
