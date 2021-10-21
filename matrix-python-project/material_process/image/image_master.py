import sys, os, time, json, shutil, pymysql, pika, requests, traceback
sys.path.append(os.getcwd())
from db.database_handler import InstantDB
from db.redis_handler import InstantRedis
from utils.snow_id import HSIS
from tenacity import retry, wait_fixed
from PIL import Image
from volcengine.imagex.ImageXService import ImageXService
from material_process.image.image_analyze import AnalyzeImage

class ImageMaster(object):

    def __init__(self):

        with open(os.getcwd() + "/material_process/config.json", 'r') as f0:
            info = json.load(f0)

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

        self.app_id     = info["imagex"]["app_id"]
        self.app_secret = info["imagex"]["app_secret"]
        self.service_id = info["imagex"]["service_id"]
        self.prefix     = info["imagex"]["prefix"]
        self.suffix     = info["imagex"]["suffix"]

        current = os.getcwd().replace("/prod/matrix-python-project", "")
        self.db_handle = InstantDB().get_connect()
        self.redis_handle = InstantRedis().get_redis_connect()
        # 本地路径
        self.origin_path = current + "/matrix/material/image_temp/"
        self.final_path = current + "/matrix/material/image/"
        self.imagex_service = ImageXService()
        self.imagex_service.set_ak(self.app_id)
        self.imagex_service.set_sk(self.app_secret)
        self.az = AnalyzeImage()
        self.send_url = info["send_url"]

    def notice(self, msg, count, duration):
        body = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "图片整理通知",
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": msg + "\n"
                                },
                                {
                                    "tag": "text",
                                    "text": "本次整理了" + str(count) + "张图片\n"
                                },
                                {
                                    "tag": "text",
                                    "text": "整理耗时：" + duration + "\n"
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
        channel.queue_declare(queue='imageOptionalQueue', durable=True)

        channel.exchange_declare(exchange='imageOptionalExchange', durable=True, exchange_type='direct')
        # 绑定exchange和队列  exchange 使我们能够确切地指定消息应该到哪个队列去

        channel.queue_bind(exchange='imageOptionalExchange', queue='imageOptionalQueue',
                           routing_key='imageOptionalRouting')

        # channel.basic_qos(prefetch_count=1)
        # 告诉rabbitmq，用callback来接受消息

        # 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列。True，无论调用callback成功与否，消息都被消费掉
        channel.basic_consume('imageOptionalQueue', self.callback, auto_ack=False)
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
            for root, dirs, files in os.walk(self.origin_path):
                for file in files:
                    counting += 1
                    after_name = HSIS.main()

                    # 查看后缀
                    image_ext = file.split('.')[-1]

                    try:

                        # 给图片初始转码
                        target = Image.open(self.origin_path + file)
                        prop = target.width / 640

                        origin_width = target.width
                        origin_height = target.height

                        preview_height = round(target.height // prop)
                        preview_width = 640

                        if image_ext == "jpg":
                            shutil.move(self.origin_path + file, self.final_path + after_name + ".jpg")
                        else:
                            target = target.convert('RGB')
                            target.save(self.final_path + after_name + ".jpg", quality=100)
                            os.remove(self.origin_path + file)

                        target = target.resize((preview_width, preview_height), Image.ANTIALIAS)
                        target = target.convert('RGB')
                        target.save(self.final_path + after_name + "_mini.jpg", quality=75)

                        image_url_list = [self.final_path + after_name]

                        # 接收标签、打分、meta
                        pic_tag_set, pic_mark, analyze_json = self.az.tag_pic(image_url_list)

                    except Exception as e:
                        traceback.print_exc()
                        print(e)
                        continue

                    # 送入imagex进行动漫化处理
                    try:
                        assert self.service_id and self.service_id != ""
                        params = dict()
                        params['ServiceId'] = self.service_id
                        file_paths = [self.final_path + after_name + ".jpg"]
                        imagex_service = ImageXService()
                        resp = imagex_service.upload_image(params, file_paths)
                        assert resp["PluginResult"][0]["ImageUri"]
                        analyze_json["imagex"] = resp
                        time.sleep(5)
                        pic_url = self.prefix + resp["PluginResult"][0]["ImageUri"] + self.suffix
                        pic = requests.get(pic_url, timeout=120)
                        with open(self.final_path + after_name + "_color.jpg", 'wb') as f0:
                            f0.write(pic.content)
                        _target = Image.open(self.final_path + after_name + "_color.jpg")
                        _target = _target.resize((preview_width, preview_height), Image.ANTIALIAS)
                        _target.save(self.final_path + after_name + "_color_mini.jpg", quality=75)

                    except Exception as e:
                        traceback.print_exc()
                        target.save(self.final_path + after_name + "_color.jpg", quality=75)
                        target.save(self.final_path + after_name + "_color_mini.jpg", quality=75)
                        print(e)

                    # 接口智能识别打分为95分以上时，自动将图片设置为高质图片
                    if pic_mark >= 95:
                        image_type = "0"
                    else:
                        image_type = "1"

                    # 完成处理流
                    update_sql = "insert into mat_image(image_path, image_note, image_size, image_tag, image_mark, " \
                                 "image_status, image_type, is_copyright, is_show, image_meta) VALUES " \
                                 "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                 (after_name, pymysql.escape_string(file.split('.')[0]), str(origin_width) + "*" + str(origin_height),
                                 pymysql.escape_string(json.dumps(list(pic_tag_set), ensure_ascii=False)), pic_mark, "0", image_type, "0", "0",
                                 pymysql.escape_string(json.dumps(analyze_json, ensure_ascii=False)))
                    self.db_handle.modify_DB(update_sql)

            end = time.perf_counter()
            mo, so = divmod(round(end - start), 60)
            ho, mo = divmod(mo, 60)
            out_duration = "%02d时%02d分%02d秒" % (ho, mo, so)
            self.redis_handle.delete("importImage")
            self.notice("图片素材导入完成！", counting, out_duration)


if __name__ == "__main__":
    im = ImageMaster()
    im.listen()
