import os, shutil, shlex, subprocess, json, traceback


# 把所有的视频旋转为更长的那一条边为宽，比较窄的边为高
class SpinVideo(object):

    def __init__(self):

        self.path_input = "../temp_input"
        self.path_output = "../temp_output"
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

                    spin_set_list = [
                        "ffmpeg -i ",
                        "\"",
                        self.path_input,
                        file,
                        "\"",
                        " -metadata:s:v rotate=\"0\" -codec copy -y ",
                        "\"",
                        self.path_output,
                        filename,
                        ".mp4"
                        "\"",
                    ]
                    spin_set =  "".join(spin_set_list)

                    # 首次执行
                    os.system(spin_set)

                    # 删除源文件
                    shutil.move(self.path_input + file, self.path_complete + file)

                    # 存在需要二次执行的个体
                    # 采集原始素材信息
                    catch_set = f'ffprobe -of json -select_streams v -show_streams "{self.path_output + filename}"'
                    catch_json = subprocess.run(
                        shlex.split(catch_set),
                        capture_output=True,
                        encoding='utf-8',
                        errors='ignore'
                    )
                    origin_info = json.loads(catch_json.stdout)
                    if not origin_info['streams'][0]['height']:
                        print(self.path_output + filename + " is not a valid clip!")

                    origin_height = origin_info['streams'][0]['height']
                    origin_width = origin_info['streams'][0]['width']

                    if origin_width <= origin_height:
                        sec_spin_set_list = [
                            "ffmpeg -i ",
                            "\"",
                            self.path_output,
                            filename,
                            ".mp4",
                            "\"",
                            " -metadata:s:v rotate=\"90\" -codec copy -y ",
                            "\"",
                            self.path_output,
                            filename,
                            "_",
                            ".mp4"
                            "\"",
                        ]
                        sec_spin_set = "".join(sec_spin_set_list)
                        os.system(sec_spin_set)
                        os.remove(self.path_output + filename + ".mp4")
                        os.rename(self.path_output + filename + "_" + ".mp4", self.path_output + filename + ".mp4")
                except Exception as e:
                    traceback.print_exc()
                    print(e)

    # input_file应当传入绝对路径
    @staticmethod
    def get_cmd(input_file):

        is_spin_success = True
        filename, extension = os.path.splitext(input_file)

        spin_set_list = [
            "ffmpeg -i ",
            "\"",
            input_file,
            "\"",
            " -metadata:s:v rotate=\"0\" -codec copy -y ",
            "\"",
            filename,
            "_.mp4"
            "\"",
        ]
        spin_set = "".join(spin_set_list)

        # 首次执行
        os.system(spin_set)

        # 校验文件是否存在
        if not os.path.isfile(filename + "_.mp4"):
            is_spin_success = False
            return is_spin_success

        # 删除源文件
        os.remove(input_file)
        os.rename(filename + "_" + ".mp4", filename + ".mp4")

        # 存在需要二次执行的个体

        # 采集原始素材信息
        catch_set = f'ffprobe -of json -select_streams v -show_streams "{input_file}"'
        catch_json = subprocess.run(
            shlex.split(catch_set),
            capture_output=True,
            encoding='utf-8',
            errors='ignore'
        )
        origin_info = json.loads(catch_json.stdout)
        if 'streams' not in origin_info and not origin_info['streams'][0]['height']:
            print(input_file + " is not a valid clip!")
            is_spin_success = False
            return is_spin_success

        origin_height = origin_info['streams'][0]['height']
        origin_width = origin_info['streams'][0]['width']

        if origin_width <= origin_height:
            sec_spin_set_list = [
                "ffmpeg -i ",
                "\"",
                input_file,
                "\"",
                " -metadata:s:v rotate=\"90\" -codec copy -y ",
                "\"",
                filename,
                "_.mp4"
                "\"",
            ]
            sec_spin_set = "".join(sec_spin_set_list)
            print(sec_spin_set)
            os.system(sec_spin_set)

            # 校验文件是否存在
            if not os.path.isfile(filename + "_.mp4"):
                is_spin_success = False
                return is_spin_success

            os.remove(input_file)
            os.rename(filename + "_" + ".mp4", filename + ".mp4")

        return is_spin_success

if __name__ == "__main__":
    sv = SpinVideo()
    sv.main()



