import schedule, time, sys, os, traceback
sys.path.append(os.getcwd())
from sync_ytb_video.ytdl import VideoDownload

p = VideoDownload().run

schedule.every(5).days.at("04:00").do(p)
# schedule.every(1).minutes.do(p)
print("脚本已启动")

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        traceback.print_exc()
        print(e)


# building = Building()
# building.run()