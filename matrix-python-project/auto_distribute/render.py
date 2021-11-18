import requests, time, sys, os, time, json, pymysql, traceback, shutil, random

sys.path.append(os.getcwd())
from multiprocessing.managers import BaseManager
from db.db_pool_handler import InstantDBPool
from tenacity import retry, wait_fixed

# SERVER_IP = '127.0.0.1'
SERVER_PORT = 7967


class ServerManager(BaseManager):
    pass


class Render(object):

    def __init__(self, SERVER_IP):
        self.tools_handle = Tools()
        self.db_handle = InstantDBPool().get_connect()
        ServerManager.register("get_task_queue")
        self.server_manager = ServerManager(address=(SERVER_IP, SERVER_PORT), authkey=b'0')
        self.db_handle = InstantDB().get_connect()
        self.task_queue = None

    @retry(wait=wait_fixed(5))
    def start(self):
        self.server_manager.connect()
        self.task_queue = self.server_manager.get_task_queue()
        print("Client Start!")
        while True:
            instruction_set = self.task_queue.get()

            # 查库，将所有素材记录取出，如果时间长度大于1秒，说明可以淡入淡出，如果可以就处理，不行就算了。
            select_current_music_detail_sql = "SELECT audio_id, audio_path, audio_name, audio_author, audio_time FROM mat_audio " \
                                              "WHERE audio_id = '%s' LIMIT 1" % instruction_set["music_id"]
            _current_music_detail = db_handle.search(select_current_music_detail_sql)

             # 叠加音频轨道



            instruction_set[""]
