# 两个目的：1. 把所有音乐格式转为mp3 2. 将数据库和文件夹match上
# TODO 使用前测试一下ffmpeg是否对所有格式都生效

import sys, os, time, json
sys.path.append(os.getcwd())
from db.db_pool_handler import InstantDBPool
import pymysql, traceback


class Trans(object):

    def __init__(self):

        self.db_handle = InstantDBPool().get_connect()
        self.file_path = "/home/hocassian/matrix/music_collection/audio/"
        # print(self)

    def music2mp3(self):

        for root, dirs, files in os.walk(self.file_path):
            # 遍历所有文件
            for file in files:
                filename, extension = os.path.splitext(file)

                # 直接改库
                update_ext_sql = "UPDATE xiami_music set music_in_stock = '%s' where music_id = '%s'" % ("1", filename)
                try:
                    self.db_handle.modify(update_ext_sql)
                except Exception as e:
                    traceback.print_exc()
                    print(e)

                # 将自己存在的信息写入数据库
                if extension != "mp3":
                    self.trans_core(file)

    def trans_core(self, file_with_ext):
        # 使用ffmpeg转为mp3（320k）
        filename, extension = os.path.splitext(file_with_ext)
        audio_handle_set = "./ffmpeg -i \"" + self.file_path + file_with_ext + "\" -ab 320k " + self.file_path + filename + ".mp3"
        os.system(audio_handle_set)

        # TODO 删除原始资源
