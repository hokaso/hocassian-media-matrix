import sys, os, json, random, math

sys.path.append(os.getcwd())


class Mark(object):

    # 1 图片 2 模板
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def main(self):

        # 按长边对齐，返回值为被裁切掉的面积
        if self.x1 / self.y1 < self.x2 / self.y2:
            rate = self.x1 / self.x2
            mark = (self.y1 / rate - self.y2) * self.x2

        # 按高边对齐，返回值为被裁切掉的面积
        else:
            rate = self.y1 / self.y2
            mark = (self.x1 / rate - self.x2) * self.y2

        return math.fabs(mark)

    def crop(self):

        # 输入模板+图片
        # 输出放缩倍数和裁剪坐标
        if self.x1 / self.y1 < self.x2 / self.y2:
            rate = self.x1 / self.x2
            x3 = self.x2
            y3 = self.y1 / rate
            area = (0, (y3 - self.y2) / 2, x3, (y3 + self.y2) / 2)

        else:
            rate = self.y1 / self.y2
            x3 = self.x1 / rate
            y3 = self.y2
            area = ((x3 - self.x2) / 2, 0, (x3 + self.x2) / 2, y3)

        return (int(x3), int(y3)), area