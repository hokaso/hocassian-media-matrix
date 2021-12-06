import sys, os, json, shutil, traceback

sys.path.append(os.getcwd())
from bypy import ByPy
from db.db_pool_handler import InstantDBPool


class Sync2Cloud(object):

    def __init__(self):

        current = os.getcwd().replace("/prod/matrix-python-project", "")

        self.clip_resouce_path = current + "/matrix/material/video_clip/raw/"
        self.audio_resouce_path = current + "/matrix/material/audio_music/"
        self.audio_off_vocal_resouce_path = current + "/matrix/material/audio_music/audio_off_vocal/"
        self.image_resouce_path = current + "/matrix/material/image/"

        self.clip_pre_sync_path = current + "/database/matrix/material/clip/"
        self.audio_pre_sync_path = current + "/database/matrix/material/audio/"
        self.audio_off_vocal_pre_sync_path = current + "/database/matrix/material/audio/off_vocal/"
        self.image_pre_sync_path = current + "/database/matrix/material/image/"

        self.local_dir = current + "/database/material/"
        self.remote_dir = "/apps/bypy/matrix/material/"

        self.db_handle = InstantDBPool().get_connect()

    '''
    主要流程：查库，找出最新的有效资源清单，将清单上的各项记录和本地预同步文件夹中的文件记录对比，
    对比出两个list（新增项目和删除项目），再将文件复制到预同步文件夹（或者删除），
    最后将预同步文件夹和云端做一个delete_remote的单相同步操作，整体流程完成。
    '''

    def main(self):

        # ====== clip ======

        # 读取应该上传的clip内容
        should_sync_clip_sql = "select material_id, material_path from mat_clip " \
                               "where material_status = '%s' and is_copyright = '%s' and is_show = '%s' " \
                               "order by material_id" % ("0", "0", "0")

        clip_list = self.db_handle.search(should_sync_clip_sql)
        clip_path_list = [i["material_path"] + ".mp4" for i in clip_list]

        # 去对应文件夹读取文件情况
        exist_clip_path_list = []
        for clip in os.listdir(self.clip_pre_sync_path):
            if os.path.splitext(clip)[-1] == ".mp4":
                exist_clip_path_list.append(clip)

        add_list, remove_list = self.add_or_remove(clip_path_list, exist_clip_path_list)
        self.add_files_from_next(self.clip_resouce_path, self.clip_pre_sync_path, add_list)
        self.remove_files_from_exist(self.clip_pre_sync_path, remove_list)

        # ====== audio ======

        # 读取应该上传的audio内容
        should_sync_audio_sql = "select audio_id, audio_path from mat_audio " \
                                "where audio_status in('%s', '%s') and is_copyright = '%s' and is_show = '%s' " \
                                "order by audio_id" % ("0", "2", "0", "0")

        audio_list = self.db_handle.search(should_sync_audio_sql)
        audio_path_list = [i["audio_path"] + ".mp3" for i in audio_list]

        # 去对应文件夹读取文件情况
        exist_audio_path_list = []
        for audio in os.listdir(self.audio_pre_sync_path):
            if os.path.splitext(audio)[-1] == ".mp3":
                exist_audio_path_list.append(audio)

        add_list, remove_list = self.add_or_remove(audio_path_list, exist_audio_path_list)
        self.add_files_from_next(self.audio_resouce_path, self.audio_pre_sync_path, add_list)
        self.remove_files_from_exist(self.audio_pre_sync_path, remove_list)

        # ====== audio off ======

        # 读取应该上传的audio off vocal内容
        should_sync_audio_off_vocal_sql = "select audio_id, audio_path from mat_audio " \
                                          "where audio_status = '%s' and is_copyright = '%s' and is_show = '%s' " \
                                          "order by audio_id" % ("0", "0", "0")

        audio_off_list = self.db_handle.search(should_sync_audio_off_vocal_sql)
        audio_off_path_list = [i["audio_path"] + ".mp3" for i in audio_off_list]

        # 去对应文件夹读取文件情况
        exist_audio_off_path_list = []
        for audio_off in os.listdir(self.audio_off_vocal_pre_sync_path):
            if os.path.splitext(audio_off)[-1] == ".mp3":
                exist_audio_off_path_list.append(audio_off)

        add_list, remove_list = self.add_or_remove(audio_off_path_list, exist_audio_off_path_list)
        self.add_files_from_next(self.audio_off_vocal_resouce_path, self.audio_off_vocal_pre_sync_path, add_list)
        self.remove_files_from_exist(self.audio_off_vocal_pre_sync_path, remove_list)

        # ====== image ======

        # 读取应该上传的image内容
        should_sync_image_sql = "select image_id, image_path from mat_image " \
                                "where is_copyright = '%s' and is_show = '%s' " \
                                "order by image_id" % ("0", "0")

        image_list = self.db_handle.search(should_sync_image_sql)
        image_path_list = [i["image_path"] + ".jpg" for i in image_list]

        # 去对应文件夹读取文件情况
        exist_image_path_list = []
        for image in os.listdir(self.image_pre_sync_path):
            if os.path.splitext(image)[-1] == ".jpg":
                exist_image_path_list.append(image)

        add_list, remove_list = self.add_or_remove(image_path_list, exist_image_path_list)
        self.add_files_from_next(self.image_resouce_path, self.image_pre_sync_path, add_list)
        self.remove_files_from_exist(self.image_pre_sync_path, remove_list)

        # 开启同步
        bp = ByPy()
        bp.syncup(localdir = self.local_dir, remotedir = self.remote_dir, deleteremote = True)

    @staticmethod
    def add_or_remove(next_list, exist_list):

        next_set = set(next_list)
        exist_set = set(exist_list)

        add_set = list(next_set.difference(exist_set))
        remove_set = list(exist_set.difference(next_set))

        return list(add_set), list(remove_set)

    @staticmethod
    def remove_files_from_exist(file_path, file_list):
        for file in file_list:
            # 需要考虑文件不存在的情况
            try:
                print(file_path + file)
                # 危险操作，需要经过足够多的测试确定后才能放行
                # os.remove(file_path + file)
            except Exception as e:
                print(e)
                traceback.print_exc()

    @staticmethod
    def add_files_from_next(origin_file_path, target_file_path, file_list):
        for file in file_list:
            # 需要考虑文件不存在的情况
            try:
                shutil.copyfile(origin_file_path + file, target_file_path + file)
            except Exception as e:
                print(e)
                traceback.print_exc()

if __name__ == '__main__':
    sc = Sync2Cloud()
    sc.main()
