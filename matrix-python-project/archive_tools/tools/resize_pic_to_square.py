import os, time, sys

sys.path.append(os.getcwd())

from PIL import Image

class PicResize(object):

    def __init__(self, max_line):
        self.img_source_path = "temp_input/"  # 图片来源路径
        self.img_save_path = "temp_output/"  # 图片修改后的保存路径

        self.max_line = max_line
        self.image = None

    def resize2square(self, image_url, new_name):

        image = Image.open(image_url)
        # new_name = _new_name + '.jpg'
        self.image = image

        # 这个图片比较高
        if self.image.width < self.image.height:
            long_side = self.image.height
            short_side = self.image.width

            # 方体化运算
            parts = round((long_side / short_side) ** 0.5)
            # print(parts)

            # 需要开启叠叠乐模式
            if parts > 1:
                # 需要放parts排，宽度为「分段*宽边」，而高度为「最后裁出来那段贴图的高度」
                new_width = parts * self.image.width
                new_height = (self.image.height // parts) + (self.image.height % parts)
                # 新建粘贴底板
                target = Image.new('RGB', (new_width, new_height), (255, 255, 255))
                # 循环裁剪的高度和最后一段的高度有所不同（由于少了余数所以更短）
                cycle_height = self.image.height // parts
                for i in range(1, parts):
                    image_temp = self.image.crop((0, (i - 1) * cycle_height, self.image.width, i * cycle_height))
                    target.paste(image_temp, ((i - 1) * self.image.width, 0, i * self.image.width, cycle_height))
                image_temp = self.image.crop((0, self.image.height - new_height, self.image.width, self.image.height))
                target.paste(image_temp, (new_width - self.image.width, 0, new_width, new_height))

                if new_width > new_height:
                    new_long_side = new_width
                    if new_long_side > self.max_line:
                        plus = self.max_line / new_long_side
                        new_width = self.max_line
                        new_height = round(plus * new_height)
                        target = target.resize((new_width, new_height), Image.ANTIALIAS)
                else:
                    new_long_side = new_height
                    if new_long_side > self.max_line:
                        plus = self.max_line / new_long_side
                        new_width = round(plus * new_width)
                        new_height = self.max_line
                        target = target.resize((new_width, new_height), Image.ANTIALIAS)

            # 不用叠了，但高度超标
            elif self.image.height > self.max_line:
                plus = self.max_line / self.image.height
                new_width = round(plus * self.image.width)
                new_height = self.max_line
                target = image.resize((new_width, new_height), Image.ANTIALIAS)

            # 一切符合标准
            else:
                target = image

        # 这个图片比较宽
        else:
            long_side = self.image.width
            short_side = self.image.height

            # 方体化运算
            parts = round((long_side / short_side) ** 0.5)
            # print(parts)

            # 需要开启叠叠乐模式
            if parts > 1:
                # 需要放parts层，高度为「分段*竖边」，而宽度为「最后裁出来那段贴图的宽度」
                new_height = parts * self.image.height
                new_width = (self.image.width // parts) + (self.image.width % parts)
                # 新建粘贴底板
                target = Image.new('RGB', (new_width, new_height), (255, 255, 255))
                # 循环裁剪的宽度和最后一段的宽度有所不同（由于少了余数所以更短）
                cycle_width = self.image.width // parts
                for i in range(1, parts):
                    image_temp = self.image.crop(((i - 1) * cycle_width, 0, i * cycle_width, self.image.height))
                    target.paste(image_temp, (0, (i - 1) * self.image.height, cycle_width, i * self.image.height))
                image_temp = self.image.crop((self.image.width - new_width, 0, self.image.width, self.image.height))
                target.paste(image_temp, (0, new_height - self.image.height, new_width, new_height))

                if new_width > new_height:
                    new_long_side = new_width
                    if new_long_side > self.max_line:
                        plus = self.max_line / new_long_side
                        new_width = self.max_line
                        new_height = round(plus * new_height)
                        target = target.resize((new_width, new_height), Image.ANTIALIAS)
                else:
                    new_long_side = new_height
                    if new_long_side > self.max_line:
                        plus = self.max_line / new_long_side
                        new_width = round(plus * new_width)
                        new_height = self.max_line
                        target = target.resize((new_width, new_height), Image.ANTIALIAS)

            # 不用叠了，但宽度超标
            elif self.image.height > self.max_line:
                plus = self.max_line / self.image.height
                new_width = round(plus * self.image.width)
                new_height = self.max_line
                target = image.resize((new_width, new_height), Image.ANTIALIAS)

            # 一切符合标准
            else:
                target = image
        target = target.convert('RGB')
        target.save(new_name, quality=90)

        # 若超出4MB，压缩图像；其中4*1024*1024 = 4194304
        _quality = 90
        while os.path.getsize(new_name)>4194304:
            _quality = _quality - 10
            # emmmm……
            if _quality == 0:
                return False
            target.save(new_name, quality = _quality)

        return os.path.getsize(new_name)


    def run(self):
        for file in os.listdir(self.img_source_path):
            new_pic_name = int(round(time.time() * 1000))
            _ = self.resize2square(self.img_source_path + file, os.path.join(self.img_save_path, str(new_pic_name) + '.jpg'))



if __name__ == '__main__':
    test_pic = PicResize(4000)
    test_pic.run()
