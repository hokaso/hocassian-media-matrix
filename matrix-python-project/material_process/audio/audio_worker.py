import requests, time, sys, os, time, json, pymysql, traceback, shutil

sys.path.append(os.getcwd())
from multiprocessing.managers import BaseManager
from db.database_handler import InstantDB
from tenacity import retry, wait_fixed
from utils.tools import Tools

# SERVER_IP = '127.0.0.1'
SERVER_PORT = 7969


class ServerManager(BaseManager):
    pass


class AudioWorker(object):

    def __init__(self, SERVER_IP):

        current = os.getcwd().replace("/prod/matrix-python-project", "")

        ServerManager.register("get_task_queue")
        self.tools_handle = Tools()
        self.server_manager = ServerManager(address=(SERVER_IP, SERVER_PORT), authkey=b'0')
        self.db_handle = InstantDB().get_connect()
        self.local_path = current + "/matrix/material/audio_music/"
        self.off_vocal_url = current + "/matrix/material/audio_music/audio_off_vocal/"
        self.task_queue = None

    # TODO：记得加上重试三次退出的代码，然后清除redis缓存
    @retry(wait=wait_fixed(5))
    def start(self):
        self.server_manager.connect()
        self.task_queue = self.server_manager.get_task_queue()
        print("Client Start!")
        while True:
            instruction_set = self.task_queue.get()
            if instruction_set["op"] == 2:
                print("收到处理指令！")

                try:
                    instruction_set = self.task_queue.get()
                    if instruction_set is None:
                        continue
                except Exception as e:
                    print(e)
                    print("等待任务中")
                    time.sleep(30)
                    continue

                try:
                    shutil.copyfile(self.local_path + instruction_set["file_path"], instruction_set["file_path"])
                    self.optional(instruction_set["file_path"])
                    update_sql = "UPDATE mat_audio set audio_status = '0', is_show = '1' where audio_id = '%s'" % \
                                 instruction_set["audio_id"]
                    self.db_handle.modify_DB(update_sql)
                    os.remove(instruction_set["file_path"])
                except Exception as e:
                    traceback.print_exc()
                    print(e)

    def optional(self, path):
        off_vocal_set = "spleeter separate -p spleeter:2stems -o output \"" + path + "\""
        os.system(off_vocal_set)
        audio_handle_set_list = [
            "./ffmpeg -i \"",
            "output/",
            path.split(".")[0],
            "/accompaniment.wav",
            "\" -ab 320k ",
            self.off_vocal_url,
            path.split(".")[0],
            ".mp3"
        ]
        audio_handle_set = "".join(audio_handle_set_list)
        os.system(audio_handle_set)

        self.tools_handle.assert_file_exist(self.off_vocal_url + path.split(".")[0] + ".mp3")

        shutil.rmtree("output")


if __name__ == '__main__':
    aw = AudioWorker(SERVER_PORT)
    aw.start()
