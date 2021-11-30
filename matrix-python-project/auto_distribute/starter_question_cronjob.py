import schedule, time, sys, os, traceback
sys.path.append(os.getcwd())
from auto_distribute.starter_question import StarterQuestion

p = StarterQuestion().run

schedule.every(1).days.at("18:00").do(p)
# schedule.every(1).minutes.do(p)
print("脚本已启动")

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        traceback.print_exc()
        print(e)

