import sys, os, time, json
sys.path.append(os.getcwd())
from material_process.clip.clip_master import ClipMaster
from material_process.clip.clip_worker import ClipWorker
from material_process.audio.audio_master import AudioMaster
from material_process.audio.audio_worker import AudioWorker
from material_process.image.image_master import ImageMaster
from multiprocessing import Process

with open(os.getcwd() + "/material_process/config.json", 'r') as f0:
    info = json.loads(f0.read())

SERVER_IP = info["master_ip"]

class Starter(object):

    @staticmethod
    def clip_master():
        clip_master = ClipMaster()
        clip_master.listen()

    @staticmethod
    def clip_worker():
        time.sleep(5)
        clip_worker = ClipWorker(SERVER_IP)
        clip_worker.start()

    @staticmethod
    def audio_master():
        audio_master = AudioMaster()
        audio_master.listen()

    @staticmethod
    def audio_worker():
        time.sleep(5)
        audio_worker = AudioWorker(SERVER_IP)
        audio_worker.start()

    @staticmethod
    def image_master():
        image_master = ImageMaster()
        image_master.listen()

if __name__ == '__main__':
    st = Starter()
    p2 = Process(target=st.clip_worker)
    p4 = Process(target=st.audio_worker)
    p2.start()
    p4.start()
    print("开始启动")
