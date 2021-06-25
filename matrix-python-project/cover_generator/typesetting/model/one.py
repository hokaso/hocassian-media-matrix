import sys, os, time, json, random, copy
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from cover_generator.typesetting.more import More
from cover_generator.typesetting.mark import Mark
from cover_generator.typesetting.build import Build
from utils.snow_id import SnowId

sys.path.append(os.getcwd())


class One(object):

    def __init__(self):
        self.image_list = None
        self.rank_model = None
        self.tb = None

        with open("cover_generator/typesetting/style.json", 'r') as f0:
            style_config = json.loads(f0.read())

        self.model = style_config["one"]

        self.func_map = {
            1: self.single_build,
            2: self.windows_build
        }

    def single(self, image_list):
        return More(image_list, self.model[0]["unit_detail"], "11").main()

    def windows(self, image_list):
        rank_temp = More(image_list, self.model[1]["unit_detail"], "12").main()
        rank_temp["model_mark"] = rank_temp["model_mark"] * 4

        return rank_temp

    def build(self, image_list, model):
        self.tb = Image.open("cover_generator/background.jpg")
        self.image_list = image_list
        self.rank_model = model
        self.func_map[int(model["model_id"][1])]()

    def single_build(self):
        # 贴第一张图
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[0]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic = Build().build_up(image["filename"], rate, area)
        self.tb.paste(pic, (0, 0))
        Build().save(self.tb)

    def windows_build(self):
        image = self.image_list[self.rank_model["model_match"][0][1]]
        model = self.model[1]["unit_detail"][0]
        rate, area = Mark(image["width"], image["height"], model["width"], model["height"]).crop()
        pic = Build().build_up(image["filename"], rate, area)
        self.tb.paste(pic, (0, 0))
        self.tb.paste(pic, (540, 0))
        self.tb.paste(pic, (0, 720))
        self.tb.paste(pic, (540, 720))
        Build().save(self.tb)
