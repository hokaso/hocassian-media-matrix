# 该服务既是消费者，又是生产者，上文接新媒体后端发来的处理请求，下文接各具体运算单元，将任务分发给他们并行处理；
import sys, os, time, json, shutil, pymysql, pika, requests, traceback
sys.path.append(os.getcwd())
import shlex, subprocess
from multiprocessing import JoinableQueue
from multiprocessing.managers import BaseManager
from utils.snow_id import SnowId
from db.database_handler import InstantDB
from db.redis_handler import InstantRedis
from tenacity import retry, wait_fixed
from material_process.audio.audio_analzye import AudioAnalyze

# 队列通讯端口
SERVER_IP = '0.0.0.0'
SERVER_PORT = 7969

class ServerManager(BaseManager):
    pass

class AudioMaster(object):

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
        self.aa = AudioAnalyze()
        # 队列相关
        self.db_handle = InstantDB().get_connect()
        self.redis_handle = InstantRedis().get_redis_connect()
        self.task_queue = JoinableQueue()
        ServerManager.register("get_task_queue", callable=lambda: self.task_queue)
        self.server_manager = ServerManager(address=(SERVER_IP, SERVER_PORT), authkey=b'0')
        self.server_manager.start()
        # 本地路径
        self.origin_path = current + "/matrix/material/audio_music_temp/"
        self.final_path = current + "/matrix/material/audio_music/"

    def notice(self, msg, count, duration):
        body = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "音频归档通知",
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": msg + "\n"
                                },
                                {
                                    "tag": "text",
                                    "text": "本次归档了" + str(count) + "个音频素材\n"
                                },
                                {
                                    "tag": "text",
                                    "text": "归档耗时：" + duration + "\n"
                                }
                            ]
                        ]
                    }
                }
            }
        }
        r = requests.post(self.send_url, data=json.dumps(body))
        print(r)
        return r

    @retry(wait = wait_fixed(5))
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
        channel.queue_declare(queue='audioOptionalQueue', durable=True)

        channel.exchange_declare(exchange='audioOptionalExchange', durable=True, exchange_type='direct')
        # 绑定exchange和队列  exchange 使我们能够确切地指定消息应该到哪个队列去

        channel.queue_bind(exchange='audioOptionalExchange', queue='audioOptionalQueue',
                           routing_key='audioOptionalRouting')

        # channel.basic_qos(prefetch_count=1)
        # 告诉rabbitmq，用callback来接受消息

        # 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列。True，无论调用callback成功与否，消息都被消费掉
        channel.basic_consume('audioOptionalQueue', self.callback, auto_ack=False)
        channel.start_consuming()

    # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
    def callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(properties)
        print(body.decode())
        raw_msg = json.loads(body.decode())

        if raw_msg["optional_id"] == 1:
            print("收到导入指令！")
            start = time.perf_counter()
            counting = 0
            # 导入
            for root, dirs, files in os.walk(self.origin_path):
                for file in files:
                    counting += 1
                    try:
                        # 生成素材新文件名
                        after_name = str(SnowId(1, 2, 0).get_id())[1:]

                        # 读取文件名获取歌曲和歌手信息（存在获取不到的情况），规则为名称在前作者名在后，通过「 - 」连接
                        audio_info = file.split(" - ")
                        audio_name = ""
                        audio_author = ""
                        if len(audio_info) == 1:
                            audio_name = audio_info[0].split(".")[0]
                        elif len(audio_info) > 1:
                            audio_name = audio_info[0]
                            audio_author = audio_info[1].split(".")[0]

                        # 查看后缀并转码
                        audio_ext = file.split('.')[-1]
                        if audio_ext == "mp3":
                            shutil.move(self.origin_path + file, self.final_path + after_name + ".mp3")
                        else:
                            audio_handle_set = "./ffmpeg -i \""+ self.origin_path + file +"\" -ab 320k " + self.final_path + after_name + ".mp3"
                            os.system(audio_handle_set)

                        audio_set, analyze_json = self.aa.run(self.final_path + after_name + ".mp3")

                        # 采集处理完成的素材的信息
                        catch_set = f'./ffprobe -of json -select_streams v -show_format "{self.final_path + after_name + ".mp3"}"'
                        catch_json = subprocess.run(shlex.split(catch_set), capture_output=True, encoding='utf-8', errors='ignore')
                        after_info = json.loads(catch_json.stdout)

                        # 提取素材时长
                        duration_temp = round(float(after_info['format']['duration']))
                        m, s = divmod(duration_temp, 60)
                        duration = "%02d:%02d" % (m, s)

                        # 录入数据
                        insert_audio_sql = "INSERT INTO mat_audio(audio_path, audio_name, audio_author, audio_type, " \
                                           "audio_status, audio_emotion, audio_time, is_copyright, is_show, audio_meta) VALUES " \
                                          "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                          (after_name, pymysql.escape_string(audio_name), pymysql.escape_string(audio_author), '0', '2',
                                           pymysql.escape_string(json.dumps(list(audio_set), ensure_ascii=False)),
                                           duration, '1', '0', pymysql.escape_string(json.dumps(analyze_json, ensure_ascii=False)))
                        self.db_handle.modify_DB(insert_audio_sql)

                        if audio_ext != "mp3":
                            os.remove(self.origin_path + file)

                    except Exception as e:
                        traceback.print_exc()
                        print(e)

            end = time.perf_counter()
            mo, so = divmod(round(end - start), 60)
            ho, mo = divmod(mo, 60)
            out_duration = "%02d时%02d分%02d秒" % (ho, mo, so)
            self.redis_handle.delete("importAudio")
            self.notice("音频素材导入完成！", counting, out_duration)

        elif raw_msg["optional_id"] == 2:
            start = time.perf_counter()
            # 整理
            prepare_sql = "SELECT audio_id, audio_path, audio_time from mat_audio where audio_status = '1' or audio_status = '3'"
            all_prepared_audios = self.db_handle.search_DB(prepare_sql)
            update_status_sql = "UPDATE mat_audio set audio_status = '3', is_show = '1' where audio_status = '1'"
            self.db_handle.modify_DB(update_status_sql)
            counting = 0

            for ikey in all_prepared_audios:
                counting += 1
                instruction_set = {
                    "audio_id": ikey["audio_id"],
                    "file_path": ikey["audio_path"] + ".mp3",
                    "audio_time": ikey["audio_time"],
                    "op": 2
                }
                self.task_queue.put(instruction_set)

            self.task_queue.join()
            end = time.perf_counter()
            m, s = divmod(round(end - start), 60)
            h, m = divmod(m, 60)
            duration = "%02d时%02d分%02d秒" % (h, m, s)
            self.redis_handle.delete("batchAudio")
            self.notice("音频素材处理完成！", counting, duration)

if __name__ == "__main__":
    am = AudioMaster()
    am.listen()
