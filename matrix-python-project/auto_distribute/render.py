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



            # 查找这些记录中得分最高的前三分之一，random一个作为封面


            # 生成封面图的文字模板，方便叠加


            #

            # 将首尾两个素材渲染成淡入淡出，然后整体结合


             # 叠加音频轨道



            instruction_set[""]
