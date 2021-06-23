# 在M*N的棋盘上摆放N个元帅（M>=N），棋盘上每个方格有特定的值，每个元帅之间都不能处于同一行和同一列，求所有元帅所在的方格的值相加最小的那种摆法，以及这个最小值为多少。

import copy, random, sys, time
from munkres import Munkres, print_matrix


# 时间复杂度O(n!)
class SelectAlgorithmWithDFS(object):

    def __init__(self, _row, _column, _matrix):

        # 初始化数据
        self.row = _row
        self.column = _column
        self.matrix = _matrix

        # min的初始值
        self.min_size = sys.maxsize

        # 根据上述测试数据生成哈希表
        self.local_matrix = [[0 for _ in range(_column)] for _ in range(_row)]

        # 通过该三维数组记录寻找最优解的过程
        self.fin_matrix = []

        # 记录最优解
        self.fin_size = []

        # 计算总递归次数
        self.count = 0

    def check(self, __column):

        # 检查行列
        for k in range(self.row - 1):
            if self.local_matrix[k][__column] == 1:
                return False
        return True

    def find_min(self, _row, _min):

        if _row > self.row - 1:

            if _min < self.min_size:
                self.min_size = _min
                self.fin_size.append(self.min_size)
                self.fin_matrix.append(copy.deepcopy(self.local_matrix))

        for _column in range(self.column):
            self.count += 1
            if self.check(_column) and self.min_size > _min:
                _min = _min + self.matrix[_row][_column]
                self.local_matrix[_row][_column] = 1
                self.find_min(_row + 1, _min)
                self.local_matrix[_row][_column] = 0
                _min = _min - self.matrix[_row][_column]

    def main(self):

        start = time.perf_counter()

        # 递归入口
        self.find_min(0, 0)

        end = time.perf_counter()

        print("总递归次数：" + str(self.count))
        print("用时:" + str(end - start))

        return self.fin_matrix[-1], self.fin_size[-1]


# 时间复杂度O(2^n)
class SelectAlgorithmWithDP(object):

    def __init__(self, _row, _column, _matrix):

        # 初始化数据
        self.row = _row
        self.column = _column
        self.matrix = _matrix

        # min的初始值
        self.min_size = 0x3f3f3f3f

        # 通过该三维数组记录寻找最优解的过程
        self.fin_matrix = []

        # 记录最优解
        self.fin_size = []

        # 计算总递归次数
        self.count = 0

    # 找到最右边1的位置
    @staticmethod
    def find_right_one(num):
        if num == 0:
            return -1
        i = 0
        while num:
            if num & 1:
                return i
            num >>= 1
            i += 1

    def main(self):
        # dp[row][status][2]
        # dp[row][status][0] 在1~row层，列占用情况的二进制位status的时候，[0]存放当前最优状态（初始化最大值INF，表示不合法 or 未探索到），[1]存放当前最优状态由上一层的哪个最优状态转移而来（回溯标记）
        dp = [[[self.min_size, -1] for i in range(pow(2, self.column))] for j in range(self.row)]
        # 第1行特殊处理，避免之后行数 - 1 < 0 越界了
        for j in range(self.column):
            dp[0][1 << j][0] = self.matrix[0][j]  # 第0行只能取一个，直接赋值即可。
            # 因为是第一层，所以dp[][][1]不需要更新标记

        # 从第二行开始到最后一行，如果只有一行的话会有坑，所以上面要特殊处理一下
        for i in range(1, self.row):
            # 用status的二进制枚举1~i行的列占用情况
            for status in range(pow(2, self.column)):
                # 查看status二进制每一位的情况
                for j in range(self.column):
                    # 当前位为1，说明当前位置被占用了，要考虑是第i行的第j位要不要取用
                    if status & (1 << j) != 0:
                        # 如果取用第i行的第j位的数字能获得更大收益
                        if dp[i - 1][status ^ (1 << j)][0] + self.matrix[i][j] <= dp[i][status][0]:
                            # 更新当前最优值
                            dp[i][status][0] = dp[i - 1][status ^ (1 << j)][0] + self.matrix[i][j]
                            # 更新回溯标记，表明是从上一层哪个状态转移过来的
                            dp[i][status][1] = status ^ (1 << j)

                # 不管当前位置的是否取数，都需要考虑当前行不取任何数字，直接进行转移即可。
                if dp[i - 1][status][0] <= dp[i][status][0]:
                    # 更新当前最优值
                    dp[i][status][0] = dp[i - 1][status][0]
                    # 更新回溯标记，表明是从上一层哪个状态转移过来的
                    dp[i][status][1] = status

        # 获取答案最小值

        # 初始化答案为最大值
        ans = self.min_size
        # 答案最优的时候的列占用状态
        ans_status = 0
        # 枚举最后一行的所有状态
        for status in range(pow(2, self.column)):
            # 最后一行，且放了可放的最大数量的皇后，才有可能是答案
            if bin(status).count('1') == min(self.column, self.row):
                # 如果当前这个状态比之前的答案更优
                if dp[self.column - 1][status][0] <= ans:
                    # 更新当前最优值
                    ans = dp[self.column - 1][status][0]
                    # 更新最优值的情况下，列占用状态
                    ans_status = status

        # 根据最小值的状态回溯获得步骤（二进制）

        # 从最后一行开始
        ans_step_bin = [ans_status]
        # 从最后一行往第二行回溯
        for i in range(self.row - 1, 0, -1):
            # 队头插入上一层的状态
            ans_step_bin.insert(0, dp[i][ans_status][-1])
            # 异或一下就可以知道当前这一层取了哪里的数字
            ans_step_bin[1] = ans_step_bin[0] ^ ans_step_bin[1]
            # 往回走一步
            ans_status = dp[i][ans_status][-1]

        # 将获得的二进制的步骤转化为十进制数字（从0开始）
        ans_step = []
        for i in range(self.row):
            ans_step.insert(i, self.find_right_one(ans_step_bin[i]))
        # print(ans_step)

        # 输出具体方案(二进制图)
        # for i in range(self.row):
        #     print(bin(ans_step_bin[i])[2:].zfill(self.column)[::-1])

        # 返回答案
        return ans, ans_step


# 时间复杂度O(n^3)
class SelectAlgorithmWithKM(object):

    def __init__(self, _matrix):
        # 初始化数据
        self.matrix = _matrix

        # min的初始值
        self.min_size = sys.maxsize

    def main(self):
        # start = time.perf_counter()
        m = Munkres()
        indexes = m.compute(self.matrix)
        # print_matrix(self.matrix, msg='Lowest cost through this matrix:')
        total = 0
        # print(indexes)
        for _row, _column in indexes:
            value = self.matrix[_row][_column]
            total += value
            # print(f'({row}, {column}) -> {value}')
        # print(f'total cost: {total}')
        # end = time.perf_counter()
        # print("用时:" + str(end - start))

        return indexes, total


if __name__ == '__main__':
    # 列数（N）
    row = 1

    # 行数（M）
    column = 8

    # 随机生成一组测试数据
    matrix = [[random.random() for j in range(column)] for i in range(row)]

    sa = SelectAlgorithmWithDFS(row, column, matrix)
    print(sa.main())

    # sa = SelectAlgorithmWithDP(row, row, matrix)
    # print(sa.main())

    sa = SelectAlgorithmWithKM(matrix)
    print(sa.main())
