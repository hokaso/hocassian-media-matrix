import schedule, time, sys, os
sys.path.append(os.getcwd())

p = VideoDownload().run

schedule.every(5).days.at("04:00").do(p)
# schedule.every(1).minutes.do(p)
print("脚本已启动")

while True:
    schedule.run_pending()
    time.sleep(1)


