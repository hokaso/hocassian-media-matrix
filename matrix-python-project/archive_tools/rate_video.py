import os, shutil, shlex, subprocess, json, traceback

RATE_VALUE = 30
CRF_VALUE = 20

# 把所有视频转成统一的帧数
class RateVideo(object):

    def __init__(self):
        self.path_input = "./temp_input"
        self.path_output = "./temp_output"
        self.path_complete = "./complete"

    def main(self):

        # 访问指定文件夹(假设视频都放在这里面)
        for root, dirs, files in os.walk(self.path_input):
            # 遍历所有文件
            for file in files:
                try:
                    filename, extension = os.path.splitext(file)

                    # 采集原始素材信息
                    catch_set = f'./ffprobe -of json -select_streams v -show_streams "{self.path_input + file}"'
                    catch_json = subprocess.run(shlex.split(catch_set), capture_output=True, encoding='utf-8',
                                                errors='ignore')
                    origin_info = json.loads(catch_json.stdout)

                    # 为何不判断素材后缀？因为如果这不是一个视频素材，这一步就会直接报错走人
                    assert origin_info['streams'][0]['height']

                    rate_set_list = [
                        "ffmpeg -r ",
                        str(RATE_VALUE),
                        " -i ",
                        "\"",
                        self.path_input,
                        "/",
                        file,
                        "\"",
                        " -crf ",
                        str(CRF_VALUE),
                        " \"",
                        self.path_output,
                        "/",
                        filename,
                        ".mp4"
                        "\"",
                    ]
                    rate_set =  "".join(rate_set_list)
                    os.system(rate_set)

                    # 移动已完成的源文件
                    shutil.move(self.path_input + file, self.path_complete + file)
                except Exception as e:
                    traceback.print_exc()
                    print(e)


if __name__ == "__main__":
    rv = RateVideo()
    rv.main()
