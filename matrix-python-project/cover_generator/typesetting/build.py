import sys, os, time, json, random, copy, traceback
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from utils.snow_id import SnowId

sys.path.append(os.getcwd())

class Build(object):

    # origin：原图文件夹
    # render：拼图文件夹
    def __init__(self, origin, render):
        self.url = "cover_generator/"+ origin +"/"
        self.render = "cover_generator/" + render +"/"

    # 传回来的应该是一个PIL的图片对象
    def build_up(self, image, rate, area):
        try:
            pic = Image.open(self.url + image)
            pic = pic.resize(rate, Image.ANTIALIAS)
            pic = pic.crop(area)
        except Exception as e:
            traceback.print_exc()
            print(e)
            raise

        # pic.save(str(SnowId(1, 2, 0).get_id())[1:] + '.jpg', quality=100)
        return pic

    def save(self, tb):
        tb.save(self.render + str(SnowId(1, 2, 0).get_id())[1:] + '.jpg', quality=100)

