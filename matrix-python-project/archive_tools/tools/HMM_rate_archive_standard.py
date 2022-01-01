# Hocassian material matrix rate archive standard
# 此标准沿用同和素材矩阵对于不同帧率视频的统一原则，即：0~45fps：30fps、46~55fps：50fps、56~65fps：60fps、66fps以上：30fps

import sys, os, time, json
sys.path.append(os.getcwd())

class HMM(object):

    @staticmethod
    def individual_standard(origin_rate_value):
        if origin_rate_value:
            if 0 < origin_rate_value <= 45 or origin_rate_value >= 66:
                after_rate = 30
            elif 46 < origin_rate_value <= 55:
                after_rate = 50
            elif 56 < origin_rate_value <= 65:
                after_rate = 60
            else:
                after_rate = 30
        else:
            after_rate = 30

        print("帧率从"+ origin_rate_value +"调整为" + after_rate)

        return after_rate

    # 如果是归档模式，则只分30和60
    @staticmethod
    def archive_standard(origin_rate_value):
        if origin_rate_value:
            if 0 < origin_rate_value <= 45 or origin_rate_value >= 66:
                after_rate = 30
            elif 46 < origin_rate_value <= 55:
                after_rate = 60
            elif 56 < origin_rate_value <= 65:
                after_rate = 60
            else:
                after_rate = 30
        else:
            after_rate = 30

        print("帧率从" + str(origin_rate_value) + "调整为" + str(after_rate))

        return after_rate

if __name__ == "__main__":
    hmm = HMM()
    hmm.individual_standard("30")


