import os, cv2


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
                    spin_set_list = [
                        "ffmpeg -i ",
                        self.path_input,
                        "/",
                        file,
                        " -metadata:s:v rotate=\"0\" -codec copy -y ",
                        self.path_output,
                        "/",
                        filename,
                        ".mp4"
                    ]
                    spin_set =  "".join(spin_set_list)
                    # 首次执行
                    os.system(spin_set)

                    # 存在需要二次执行的个体
                    capture = cv2.VideoCapture(self.path_output + "/" + filename + ".mp4")
                    width = capture.get(3)
                    height = capture.get(4)
                    capture.release()
                    if width <= height:
                        sec_spin_set_list = [
                            "ffmpeg -i ",
                            self.path_output,
                            "/",
                            filename,
                            ".mp4",
                            " -metadata:s:v rotate=\"90\" -codec copy -y ",
                            self.path_output,
                            "/",
                            filename,
                            "_",
                            ".mp4"
                        ]
                        sec_spin_set = "".join(sec_spin_set_list)
                        os.system(sec_spin_set)
                        os.remove(self.path_output + "/" + filename + ".mp4")


if __name__ == "__main__":
    rv = RateVideo()
    rv.main()



