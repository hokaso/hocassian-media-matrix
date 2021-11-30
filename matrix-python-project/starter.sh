# 按需启动

# 开启油管视频同步脚本
screen_name="ytb"
sudo screen -dmS $screen_name
sudo screen -x -S $screen_name -p 0 -X stuff $'cd /home/hocassian/prod/matrix-python-project\nsudo python3 sync_ytb_video/ytb_update_clock.py\n'

# 开启素材矩阵渲染服务端
screen_name="starter"
screen -dmS $screen_name
screen -x -S $screen_name -p 0 -X stuff $'cd ~/prod/matrix-python-project\npython3 material_process/starter.py\n'

# 开启封面生成助手后端
screen_name="lark"
screen -dmS $screen_name
screen -x -S $screen_name -p 0 -X stuff $'cd ~/prod/matrix-python-project\npython3 cover_generator/lark.py\n'

# 开启封面生成助手垃圾回收
screen_name="lark_cycle"
screen -dmS $screen_name
screen -x -S $screen_name -p 0 -X stuff $'cd ~/prod/matrix-python-project\npython3 cover_generator/operator.py\n'

# 开启分发矩阵定时提醒
screen_name="distribute_cronjob"
screen -dmS $screen_name
screen -x -S $screen_name -p 0 -X stuff $'cd ~/prod/matrix-python-project\npython3 auto_distribute/starter_question_cronjob.py\n'

# 开启分发矩阵server端
screen_name="distribute_server"
screen -dmS $screen_name
screen -x -S $screen_name -p 0 -X stuff $'cd ~/prod/matrix-python-project\npython3 auto_distribute/flow_questions.py\n'

# 开启分发矩阵client端
screen_name="distribute_client"
screen -dmS $screen_name
screen -x -S $screen_name -p 0 -X stuff $'cd ~/prod/matrix-python-project\npython3 auto_distribute/render.py\n'
