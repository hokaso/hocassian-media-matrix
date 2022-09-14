import sys, os, time, json

sys.path.append(os.getcwd())


def hump_to_underline(text):
    res = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            res.append("_")
        res.append(char)
    return ''.join(res).lower()


def underline_hump(text):
    arr = text.lower().split('_')
    res = []
    for i in arr:
        res.append(i[0].upper() + i[1:])
    return ''.join(res)


class Run(object):

    def __init__(self):

        # 此处请填入驼峰命名
        self.method_name = "Horizontal2Vertical"
        _method_name_abbr = ""

        for i in self.method_name:
            if i.isupper():
                _method_name_abbr += i

        self.method_name_abbr = _method_name_abbr.lower()

        self.method_filename = hump_to_underline(self.method_name)

        with open("method_model.txt", 'r') as f0:
            self.method_model = f0.read()

    def run(self):

        _sm = self.method_model
        sm = _sm.replace("{method_name}", self.method_name).replace("{method_name_abbr}", self.method_name_abbr)

        with open(self.method_filename + ".py", 'w') as f0:
            f0.write(sm)

        print(sm)
        pass


if __name__ == "__main__":
    r = Run()
    r.run()
