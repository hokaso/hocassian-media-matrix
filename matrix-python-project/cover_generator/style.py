import sys, os, time, random
from PIL import Image

sys.path.append(os.getcwd())

from cover_generator.typesetting.model.one import One
from cover_generator.typesetting.model.two import Two
from cover_generator.typesetting.model.three import Three
from cover_generator.typesetting.model.four import Four
from cover_generator.typesetting.model.five import Five
from cover_generator.typesetting.model.six import Six
# from cover_generator.typesetting.model.seven import Seven
# from cover_generator.typesetting.model.eight import Eight
# from cover_generator.typesetting.model.nine import Nine


class Style(object):

    def __init__(self, image_path):

        self.image_map = {
            # 0: self.break_out,
            1: self.one,
            2: self.two,
            3: self.three,
            4: self.four,
            5: self.five,
            6: self.six,
            # 7: self.seven,
            # 8: self.eight,
            # 9: self.nine
        }

        self.image_path = image_path

        self.build_map = {
            1: One(image_path),
            2: Two(image_path),
            3: Three(image_path),
            4: Four(image_path),
            5: Five(image_path),
            6: Six(image_path)
        }

        # "model_id": "模板编号，从左往右数第一位是父模板编号，第二位是子模板编号",
        # "model_match": "具体模板的拼接方式，比如子模板中的第一个方格存放第五张图片，具体的最优摆放路径和得分已由KM算法得出",
        # "model_mark": "当前子模板最优摆放的得分，从所有子模板里选择得分最高的前三名来渲染展示"
        self.rank_dict = []

        # self.image_path = image_path if image_path else self.image_path = "images"
        self.image_path = "cover_generator/" + image_path

        image_ext = ['.jpg', '.png', '.jpeg', '.bmp']
        self.image_list = []
        self.image_count = 0
        for root, dirs, files in os.walk(self.image_path):
            for file in files:
                if os.path.splitext(file)[-1] in image_ext:
                    self.image_count += 1
                    image = Image.open(self.image_path + "/" + file)

                    self.image_info = {
                        "filename": file,
                        "width": image.width,
                        "height": image.height,
                        "mark": 0
                    }

                    self.image_list.append(self.image_info)

    def one(self):
        self.rank_dict.append(One(self.image_path).windows(self.image_list))
        self.rank_dict.append(One(self.image_path).single(self.image_list))

    def two(self):
        self.rank_dict.append(Two(self.image_path).horizontal(self.image_list))
        self.rank_dict.append(Two(self.image_path).vertical(self.image_list))
        self.rank_dict.append(Two(self.image_path).windows(self.image_list))

    def three(self):
        self.rank_dict.append(Three(self.image_path).horizontal(self.image_list))
        self.rank_dict.append(Three(self.image_path).vertical(self.image_list))
        self.rank_dict.append(Three(self.image_path).triple_vertical(self.image_list))
        self.rank_dict.append(Three(self.image_path).triple_horizontal(self.image_list))

    def four(self):
        self.rank_dict.append(Four(self.image_path).quadruple_vertical(self.image_list))
        self.rank_dict.append(Four(self.image_path).quadruple_horizontal(self.image_list))
        self.rank_dict.append(Four(self.image_path).chairs(self.image_list))
        self.rank_dict.append(Four(self.image_path).chairs_spin(self.image_list))
        self.rank_dict.append(Four(self.image_path).h2v2(self.image_list))
        self.rank_dict.append(Four(self.image_path).h2v2_spin(self.image_list))
        self.rank_dict.append(Four(self.image_path).windows(self.image_list))
        self.rank_dict.append(Four(self.image_path).windows_vertical(self.image_list))
        self.rank_dict.append(Four(self.image_path).windows_horizontal(self.image_list))

    def five(self):
        self.rank_dict.append(Five(self.image_path).offset_vertical(self.image_list))
        self.rank_dict.append(Five(self.image_path).offset_horizontal(self.image_list))
        self.rank_dict.append(Five(self.image_path).align_vertical(self.image_list))
        self.rank_dict.append(Five(self.image_path).align_horizontal(self.image_list))
        self.rank_dict.append(Five(self.image_path).mirror(self.image_list))

    def six(self):
        self.rank_dict.append(Six(self.image_path).align_vertical(self.image_list))
        self.rank_dict.append(Six(self.image_path).align_horizontal(self.image_list))
        self.rank_dict.append(Six(self.image_path).offset_vertical_small(self.image_list))
        self.rank_dict.append(Six(self.image_path).offset_horizontal_small(self.image_list))
        self.rank_dict.append(Six(self.image_path).offset_vertical_big(self.image_list))
        self.rank_dict.append(Six(self.image_path).offset_horizontal_big(self.image_list))
        self.rank_dict.append(Six(self.image_path).arround(self.image_list))

    def render(self):
        self.rank_dict.sort(key=lambda x: x["model_mark"])

        # 测试程序
        # assert adoption > 3
        # adoption = len(self.rank_dict)
        # for ikey in range(adoption):
        #     self.build_map[int(self.rank_dict[ikey]["model_id"][0])].build(self.image_list, self.rank_dict[ikey])

        # 实际程序
        adoption = int(len(self.rank_dict) / 1.5)
        assert adoption > 3
        temp = []
        while len(temp) < 3:
            index = random.randint(0, adoption)
            if index not in temp:
                temp.append(index)

        for ikey in temp:
            self.build_map[int(self.rank_dict[ikey]["model_id"][0])].build(self.image_list, self.rank_dict[ikey])

    def run(self):

        start = time.perf_counter()
        _image_count = self.image_count

        if self.image_count > 6:
            _image_count = 6

        for i in range(_image_count):
            self.image_map[i+1]()

        self.render()

        end = time.perf_counter()
        print("用时:" + str(end - start))
        print(self.rank_dict)


