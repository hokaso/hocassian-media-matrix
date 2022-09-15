import math

'''
    输入：
    fw和fh代表素材原本的宽高，fs代表填充类型，true为适配，false为包含
    mw和mh代表模板宽高

    输出：
    tw和th代表素材经过算法处理后的宽高
    lw和lh代表素材经过算法处理后左上角应该渲染在模板中的坐标（毕竟渲染器是从上至下，从左到右来渲染，所以需要左上角坐标）
    (cw1,ch1)/(cw2,ch2)代表素材经过算法处理后素材需要裁剪的坐标，cs代表是否需要裁剪
'''


def fill(fw, fh, mw, mh):
    if all([
        fw == mw,
        fh == mh,
    ]):
        return fw, fh, 0, 0, mw, mh

    # if all([
    #     fw == self.standard_1k_w,
    #     fh == self.standard_1k_h,
    #     mw == self.standard_1k_h,
    #     mh == self.standard_1k_w,
    # ]):
    #     return 3414, 1920, 1167, 0, 2247, 1920

    if fw >= fh * mw / mh:
        th = mh
        tw = math.ceil(mh * fw / fh)

    else:
        th = math.ceil(mw * fh / fw)
        tw = mw

    cw1 = int((tw - mw) / 2)
    ch1 = int((th - mh) / 2)

    cw2 = cw1 + mw
    ch2 = ch1 + mh

    return tw, th, cw1, ch1, cw2, ch2


def adapt(fw, fh, mw, mh):
    if all([
        fw == mw,
        fh == mh,
    ]):
        return fw, fh, 0, 0

    # if all([
    #     fw == self.standard_1k_w,
    #     fh == self.standard_1k_h,
    #     mw == self.standard_1k_h,
    #     mh == self.standard_1k_w,
    # ]):
    #     return 1080, 608, 0, 656

    if fw >= fh * mw / mh:
        tw = mw
        th = math.ceil(mw * fh / fw)
        lw = 0
        lh = int((mh - th) / 2)
    else:
        tw = math.ceil(mh * fw / fh)
        th = mh
        lw = int((mw - tw) / 2)
        lh = 0

    return tw, th, lw, lh


# tp代表处理模式，1四比三 2一比一
# cx和cy代表裁剪开始的坐标
def adapt_extra(fw, fh, mw, mh, tp):
    if tp == 2:
        if fw >= fh:
            cx = int((fw - fh) / 2)
            cy = 0
            fw = fh

        else:
            cx = 0
            cy = int((fh - fw) / 2)
            fh = fw

    else:
        if fw >= fh * 4 / 3:

            nw = fh / (3 / 4)
            cx = int((fw - nw) / 2)
            cy = 0
            fw = nw

        else:

            nh = fw / (3 / 4)
            cx = 0
            cy = int((fh - nh) / 2)
            fw = nh

    tw, th, lw, lh = adapt(fw, fh, mw, mh)
    return tw, th, lw, lh, cx, cy, fw, fh


def suit(fs, fw, fh, mw, mh):
    if fs:
        return adapt(fw, fh, mw, mh)
    else:
        return fill(fw, fh, mw, mh)


class SuitableLayout(object):

    def __init__(self):
        self.standard_1k_w = 1920
        self.standard_1k_h = 1080

        self.standard_4k_w = 3840
        self.standard_4k_h = 2160


if __name__ == "__main__":
    sl = SuitableLayout()
    a = suit(False, 1920, 1080, 1080, 1920)
    print(a)
