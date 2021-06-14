# 该服务既是消费者，又是生产者，上文接新媒体后端发来的处理请求，下文接各具体运算单元，将任务分发给他们并行处理；
import pika, json, time, os, sys, requests, traceback, shutil

sys.path.append(os.getcwd())
from multiprocessing import JoinableQueue
from multiprocessing.managers import BaseManager
from db.database_handler import InstantDB
from db.redis_handler import InstantRedis
from tenacity import retry, wait_fixed

# 队列通讯端口
SERVER_IP = '0.0.0.0'
SERVER_PORT = 7968


class ServerManager(BaseManager):
    pass


class ClipMaster(object):

    def __init__(self):

        with open(os.getcwd() + "/material_process/config.json", 'r') as f0:
            info = json.loads(f0.read())

        # self.ip           = info["local_dev"]["ip"]
        # self.port         = info["local_dev"]["port"]
        # self.account      = info["local_dev"]["account"]
        # self.password     = info["local_dev"]["password"]
        # self.virtual_host = info["local_dev"]["virtual_host"]

        self.ip           = info["local_prod"]["ip"]
        self.port         = info["local_prod"]["port"]
        self.account      = info["local_prod"]["account"]
        self.password     = info["local_prod"]["password"]
        self.virtual_host = info["local_prod"]["virtual_host"]

        # self.ip           = info["remote_prod"]["ip"]
        # self.port         = info["remote_prod"]["port"]
        # self.account      = info["remote_prod"]["account"]
        # self.password     = info["remote_prod"]["password"]
        # self.virtual_host = info["remote_prod"]["virtual_host"]

        current = os.getcwd().replace("/prod/matrix-python-project", "")
        self.send_url = info["send_url"]
        self.origin_path = current + "/matrix/material/video_clip_temp"
        self.final_path = current + "/matrix/material/video_clip"
        self.db_handle = InstantDB().get_connect()
        self.redis_handle = InstantRedis().get_redis_connect()
        self.task_queue = JoinableQueue()
        ServerManager.register("get_task_queue", callable=lambda: self.task_queue)
        self.server_manager = ServerManager(address=(SERVER_IP, SERVER_PORT), authkey=b'0')
        self.server_manager.start()
        self.video_ext = ["mp4", "mxf", "mov", "mpeg", "mpg", "avi", "flv", "mkv", "ogg", "3gp", "wmv", "h264", "m4v", "webm"]

    @retry(wait=wait_fixed(5))
    def listen(self):
        credentials = pika.PlainCredentials(
            self.account,
            self.password
        )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.ip,
                port=self.port,
                virtual_host=self.virtual_host,
                credentials=credentials
            )
        )
        channel = connection.channel()

        # 创建临时队列，队列名传空字符，consumer关闭后，队列自动删除
        channel.queue_declare(queue='clipOptionalQueue', durable=True)

        channel.exchange_declare(exchange='clipOptionalExchange', durable=True, exchange_type='direct')
        # 绑定exchange和队列  exchange 使我们能够确切地指定消息应该到哪个队列去

        channel.queue_bind(exchange='clipOptionalExchange', queue='clipOptionalQueue',
                           routing_key='clipOptionalRouting')

        # channel.basic_qos(prefetch_count=1)
        # 告诉rabbitmq，用callback来接受消息

        # 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列。True，无论调用callback成功与否，消息都被消费掉
        channel.basic_consume('clipOptionalQueue', self.callback, auto_ack=False)
        channel.start_consuming()

    def notice(self, msg, count, duration):
        body = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "视频转码通知",
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": msg + "\n"
                                },
                                {
                                    "tag": "text",
                                    "text": "本次转码了" + str(count) + "个素材\n"
                                },
                                {
                                    "tag": "text",
                                    "text": "转码耗时：" + duration + "\n"
                                }
                            ]
                        ]
                    }
                }
            }
        }
        try:
            r = requests.post(self.send_url, data=json.dumps(body))
        except Exception as e:
            traceback.print_exc()
            print(e)
            return None
        return r

    def output_notice(self, msg, count, duration):
        body = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "视频导出通知",
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": msg + "\n"
                                },
                                {
                                    "tag": "text",
                                    "text": "本次导出了" + str(count) + "个素材\n"
                                },
                                {
                                    "tag": "text",
                                    "text": "导出耗时：" + duration + "\n"
                                }
                            ]
                        ]
                    }
                }
            }
        }
        try:
            r = requests.post(self.send_url, data=json.dumps(body))
        except Exception as e:
            traceback.print_exc()
            print(e)
            return None
        return r

    # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
    def callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(properties)
        print(body.decode())
        raw_msg = json.loads(body.decode())

        if raw_msg["optional_id"] == 1:
            start = time.perf_counter()
            counting = 0
            # 导入
            for root, dirs, files in os.walk(self.origin_path):
                for file in files:
                    counting += 1
                    _file_ext = file.split('.')[-1]
                    file_ext = _file_ext.lower()
                    # print(file)
                    if file_ext in self.video_ext:
                        instruction_set = {
                            "file_path": file,
                            "op": 1
                        }
                        print(instruction_set)
                        self.task_queue.put(instruction_set)

            self.task_queue.join()
            end = time.perf_counter()
            m, s = divmod(round(end - start), 60)
            h, m = divmod(m, 60)
            duration = "%02d时%02d分%02d秒" % (h, m, s)
            self.redis_handle.delete("importClip")
            self.notice("视频素材导入处理完成！", counting, duration)

        elif raw_msg["optional_id"] == 2:
            start = time.perf_counter()
            # 整理
            prepare_sql = "SELECT material_id, material_path, material_type, material_start, material_end from mat_clip " \
                          "where material_status = '3' or material_status = '2'"
            all_prepared_clips = self.db_handle.search_DB(prepare_sql)
            update_status_sql = "UPDATE mat_clip set material_status = '2' where material_status = '3'"
            self.db_handle.modify_DB(update_status_sql)
            counting = 0
            for ikey in all_prepared_clips:
                counting += 1
                instruction_set = {
                    "material_id": ikey["material_id"],
                    "file_path": ikey["material_path"],
                    "material_type": ikey["material_type"],
                    "start": ikey["material_start"],
                    "end": ikey["material_end"],
                    "op": 2
                }
                self.task_queue.put(instruction_set)

            self.task_queue.join()
            end = time.perf_counter()
            m, s = divmod(round(end - start), 60)
            h, m = divmod(m, 60)
            duration = "%02d时%02d分%02d秒" % (h, m, s)
            self.redis_handle.delete("batchClip")
            self.notice("视频素材裁切处理完成！", counting, duration)

        elif raw_msg["optional_id"] == 3:
            time.sleep(3)
            start = time.perf_counter()
            prepare_sql = "SELECT material_id, material_path from mat_clip " \
                          "where material_status = '4'"
            all_prepared_clips = self.db_handle.search_DB(prepare_sql)

            if not os.path.exists(self.final_path + "/output"):
                os.makedirs(self.final_path + "/output")

            current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

            current_folder = self.final_path + "/output/" + current_time
            os.makedirs(current_folder)
            os.makedirs(current_folder + "/proxies")

            counting = 0

            for ikey in all_prepared_clips:

                counting += 1
                # 複製原始文件
                shutil.copyfile(self.final_path + "/raw/" + ikey["material_path"] + ".mp4", current_folder + "/" + ikey["material_path"] + ".mp4")
                # 複製代理文件
                shutil.copyfile(self.final_path + "/preview/" + ikey["material_path"] + ".mp4", current_folder + "/proxies/" + ikey["material_path"] + ".mp4")

                reduction_sql = "UPDATE mat_clip set material_status = '0' where material_id = '%s'" % (ikey["material_id"])
                self.db_handle.modify_DB(reduction_sql)

            self.task_queue.join()
            end = time.perf_counter()
            m, s = divmod(round(end - start), 60)
            h, m = divmod(m, 60)
            duration = "%02d时%02d分%02d秒" % (h, m, s)
            self.redis_handle.delete("translateClip")
            self.output_notice("视频导出完成！", counting, duration)



if __name__ == '__main__':
    clip_master = ClipMaster()
    clip_master.listen()
