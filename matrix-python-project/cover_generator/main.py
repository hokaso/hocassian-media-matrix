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

    def run_test(self):
        Style(None).run()

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


    @staticmethod
    def run(record_id, first_title, secord_title):

        Style(record_id).run()
        image_list = []
        image_ext = ['.jpg', '.png', '.jpeg', '.bmp']
        for root, dirs, files in os.walk(record_id):
            for file in files:
                if os.path.splitext(file)[-1] in image_ext:
                    image = Image.open(record_id + "_temp/" + file)
                    Structure().run(first_title, secord_title)
                    title = Image.open("transparent_title.png")
                    r, g, b, a = title.split()
                    image.paste(title, (0, 0), mask=a)
                    new_image_name = record_id + "_fin/" + str(SnowId(1, 2, 0).get_id())[1:] + '.png'
                    image.save(new_image_name, quality=100)
                    image_list.append(new_image_name)

        return image_list


if __name__ == "__main__":
    m = Main()
    m.run_test()
