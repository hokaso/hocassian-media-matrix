from cover_generator.typesetting.select_algorithm import SelectAlgorithmWithKM
from cover_generator.typesetting.mark import Mark

class More(object):

    def __init__(self, column, row, model_id):

        self._column = column
        self._row = row
        self._model_id = model_id

    def main(self):

        bag_matrix = [[0 for _ in range(len(self._column))] for _ in range(len(self._row))]

        for i, image in enumerate(self._row):
            for j, model in enumerate(self._column):
                bag_matrix[i][j] = Mark(image["width"], image["height"], model["width"], model["height"]).main()

        sa = SelectAlgorithmWithKM(bag_matrix)

        # ([(0, 2), (1, 1), (2, 3), (3, 4), (4, 7), (5, 13), (6, 5), (7, 8), (8, 9)]
        # 表示0号模板对应第2张图片，1号模板对应第1张图片……
        min_path, min_mark = sa.main()

        rank_temp = {"model_id": self._model_id, "model_match": min_path, "model_mark": min_mark}

        return rank_temp