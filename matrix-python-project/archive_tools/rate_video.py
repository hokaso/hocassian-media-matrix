import os, shutil


class RateVideo(object):

    def __init__(self):
        self.path_input = "./temp_input"
        self.path_output = "./temp_output"

    def main(self):

        # 访问指定文件夹(假设视频都放在这里面)
        for root, dirs, files in os.walk(self.path_input):
            # 遍历所有文件
            for file in files:
                # 如果后缀名为 .mp4
                filename, extension = os.path.splitext(file)
                if extension == '.mp4':
                    rate_set_list = [
                        "ffmpeg -r 30 -i ",
                        self.path_input,
                        "/",
                        file,
                        " -crf 20 ",
                        self.path_output,
                        "/",
                        filename,
                        ".mp4"
                    ]
                    rate_set =  "".join(rate_set_list)
                    os.system(rate_set)


if __name__ == "__main__":
    rv = RateVideo()
    rv.main()
