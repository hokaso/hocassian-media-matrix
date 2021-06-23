import sys, os, time, json

sys.path.append(os.getcwd())
from cover_generator.structure import Structure
from cover_generator.style import Style
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from utils.snow_id import SnowId


class Main(object):

    def __init__(self):

        self.image_path = "render"

        # 主标题限定7字
        self.test_title = "测试文案试测试"
        # 副标题限定11字
        self.test_secord_title = "测试副标题测试副标题测"
        # self.db_handle = InstantDB().get_conncet()

    def run(self):
        Style().run()

        image_ext = ['.jpg', '.png', '.jpeg', '.bmp']
        for root, dirs, files in os.walk(self.image_path):
            for file in files:
                if os.path.splitext(file)[-1] in image_ext:
                    image = Image.open("render/" + file)
                    Structure().run(self.test_title, self.test_secord_title)
                    title = Image.open("transparent_title.png")
                    r, g, b, a = title.split()
                    image.paste(title, (0, 0), mask=a)
                    image.save("fin/" + str(SnowId(1, 2, 0).get_id())[1:] + '.png', quality=100)
                    os.remove("render/" + file)


if __name__ == "__main__":
    m = Main()
    m.run()
