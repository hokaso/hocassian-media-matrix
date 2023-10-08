# 此方法用于补上之前没打标签的音乐，毕竟现在接口恢复了~
import sys, os, time, json, shutil, pymysql, pika, requests, traceback
sys.path.append(os.getcwd())

from db.db_pool_handler import InstantDBPool
from material_process.audio.audio_analzye import AudioAnalyze

class AudioTagMakeUp(object):

    def __init__(self):

        with open(os.getcwd() + "/material_process/config.json", 'r') as f0:
            info = json.load(f0)

        self.ip = info["local_prod"]["ip"]
        self.port = info["local_prod"]["port"]
        self.account = info["local_prod"]["account"]
        self.password = info["local_prod"]["password"]

        self.aa = AudioAnalyze()
        self.db_handle = InstantDBPool().get_connect()

        current = os.getcwd().replace("/prod/matrix-python-project", "")
        self.final_path = current + "/matrix/material/audio_music/"

    def executor(self):

        find_all_tag_empty_sql = "select audio_path from mat_audio where audio_emotion = '[]'"
        all_tag_empty_records = self.db_handle.search(find_all_tag_empty_sql)
        print(all_tag_empty_records)

        for ikey in all_tag_empty_records:
            audio_set, analyze_json = self.aa.run(self.final_path + ikey["audio_path"] + ".mp3")
            print(audio_set)

            # 录入数据
            update_audio_sql = "UPDATE mat_audio set audio_emotion = '%s', audio_meta = '%s' where audio_path = '%s'" % \
                               (pymysql.converters.escape_string(json.dumps(list(audio_set), ensure_ascii=False)),
                                pymysql.converters.escape_string(json.dumps(analyze_json, ensure_ascii=False)),
                                ikey["audio_path"])

            self.db_handle.modify(update_audio_sql)

if __name__ == '__main__':
    AudioTagMakeUp().executor()