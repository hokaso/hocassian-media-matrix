import sys, os, time, json, random, copy
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from utils.snow_id import SnowId

sys.path.append(os.getcwd())

class Build(object):

    def __init__(self):
        self.url = "images/"

    # 传回来的应该是一个PIL的图片对象
    def build_up(self, image, rate, area):

        pic = Image.open(self.url + image)
        pic = pic.resize(rate, Image.ANTIALIAS)
        pic = pic.crop(area)
        # pic.save(str(SnowId(1, 2, 0).get_id())[1:] + '.jpg', quality=100)

        return pic

    @staticmethod
    def save(tb):
        tb.save("render/" + str(SnowId(1, 2, 0).get_id())[1:] + '.jpg', quality=100)

