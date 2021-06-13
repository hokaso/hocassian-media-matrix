import sys, os, time
sys.path.append(os.getcwd())
from material_process.clip.clip_master import ClipMaster
from material_process.clip.clip_worker import ClipWorker
from material_process.audio.audio_master import AudioMaster
from material_process.audio.audio_worker import AudioWorker
from material_process.image.image_master import ImageMaster
from multiprocessing import Process

SERVER_IP = '0.0.0.0'

class Starter(object):

    @staticmethod
    def clip_master():
        clip_master = ClipMaster(SERVER_IP)
        clip_master.listen()

    @staticmethod
    def clip_worker():
        time.sleep(5)
        clip_worker = ClipWorker()
        clip_worker.start()

    @staticmethod
    def audio_master():
        audio_master = AudioMaster()
        audio_master.listen()

    @staticmethod
    def audio_worker():
        time.sleep(5)
        audio_worker = AudioWorker()
        audio_worker.start()

    @staticmethod
    def image_master():
        image_master = ImageMaster()
        image_master.listen()

if __name__ == '__main__':
    st = Starter()
    p1 = Process(target=st.clip_master)
    p2 = Process(target=st.clip_worker)
    p3 = Process(target=st.audio_master)
    p4 = Process(target=st.audio_worker)
    p5 = Process(target=st.image_master)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    print("开始启动")