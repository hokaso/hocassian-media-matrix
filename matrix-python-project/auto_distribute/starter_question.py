import sys, os

sys.path.append(os.getcwd())
from db.db_pool_handler import InstantDBPool
from utils.tools import Tools
from auto_distribute.lark import Lark


class StarterQuestion(object):

    def __init__(self):

        self.db_handle = InstantDBPool().get_connect()
        self.msg_handle = Lark()
        self.tools_handle = Tools()

    def run(self):

        # 查库，将所有适合做视频的素材总时长加起来（新增字段：has_uploaded；0没发布过，1已经发布过）
        find_suitable_duration_sql = "select material_id, material_path, material_time from mat_clip " \
                                     "where material_status = '%s' and is_copyright = '%s' and has_uploaded = '%s'" % \
                                     ("0", "0", "0")
        clip_records = self.db_handle.search_DB(find_suitable_duration_sql)
        duration_counter = 0
        for ikey in clip_records:
            current_duration = self.tools_handle.string2timestamp(ikey["material_time"])
            if current_duration > 10:
                current_duration = 10
            duration_counter = current_duration + duration_counter

        # 如果总时长在5分钟以上，才继续工作流
        if duration_counter < 300:
            # TODO 发送消息卡片提示用户素材不够，再接再厉~（可能还需要深层次定义，不然很有可能打扰到用户；但反过来看，如果频繁提醒，其实也是对用户的一种促进）
            return 0

        # 销毁过往工作流
        destory_sql = "update flow_distribute set status = '%s'" % "0"
        self.db_handle.modify(destory_sql)

        # 创建工作流
        create_sql = "INSERT INTO flow_distribute(status) VALUES('%s')" % "1"
        last_row_id = self.db_handle.modify(create_sql)
        if not last_row_id:
            print("last_row_id为空！")
            return 0

        # 发送消息卡片
        self.msg_handle.send_starter_msg(duration_counter, last_row_id)

