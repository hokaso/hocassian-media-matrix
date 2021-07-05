# 请按需导入，将不需要的删去以提升性能
from flask import Flask, request
import os, sys, requests, json, datetime, time, pymysql, hashlib, base64, traceback, imghdr, shutil
from Crypto.Cipher import AES
from gevent import pywsgi

sys.path.append(os.getcwd())
from utils.snow_id import SnowId
from db.database_handler import InstantDB
from cover_generator.main import Main

with open("cover_generator/config.json", 'r') as f0:
    info = json.load(f0)

APP_ID = info["APP_ID"]
APP_SECRET = info["APP_SECRET"]
APP_VERIFICATION_TOKEN = info["APP_VERIFICATION_TOKEN"]
APP_ENCRYPT_KEY = info["APP_ENCRYPT_KEY"]


class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def decrypt_string(self, enc):
        enc = base64.b64decode(enc)
        return self.decrypt(enc).decode('utf8')


def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }

    try:
        rsp_body = requests.post(url, headers=headers, data=json.dumps(body))
    except Exception as e:
        print(e)
        return "fail"

    # rsp_body = response.read().decode('utf-8')
    rsp_dict = rsp_body.json()
    code = rsp_dict.get("code", -1)

    if code != 0:
        print("get tenant_access_token error, code =", code)
        return None

    return rsp_dict.get("tenant_access_token", "")


def send_msg_card(body):
    url = 'https://open.feishu.cn/open-apis/message/v4/send/'

    access_token = get_tenant_access_token()

    if access_token is None:
        return "fail"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }

    try:
        rsp_body = requests.post(url, headers=headers, data=json.dumps(body))
    except Exception as e:
        print(e.read().decode())
        return "fail"

    # rsp_body = response.read().decode('utf-8')
    rsp_dict = rsp_body.json()
    code = rsp_dict.get("code", -1)

    if code != 0:
        print("send msg error, code =", code)
        return "fail"

    return "success"


def send_init_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "请输入指令「1」后再开始上传图片~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_tip_msg(open_id):
    tip = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "欢迎使用封面生成助手："
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "○ 输入指令「1」后即可上传图片（上限为16张）\n"
                                   "○ 输入指令「2」后即可发送标题信息（7字以内，超出自动截取前7字）\n"
                                   "○ 输入指令「3」后即可发送副标题信息（11字以内，超出自动截取前11字）\n"
                                   "○ 输入指令「4」后即可执行渲染\n"
                                   "○ 输入指令「0」可终止整个流程（当图片输入有误时可用其复位）"
                    }
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": "※ 请在5分钟内完成上传，超时自动复位\n※ 在提交处理之前，可随时新增图片\n※ 暂不支持繁体中文和其他生僻字符\n※ 暂不支持gif动图与部分冷门格式"
                        }
                    ]
                }
            ]
        }
    }

    return send_msg_card(tip)


def send_fail_msg(open_id, report):
    error = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "出大问题！"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": report
                    }
                }
            ]
        }
    }

    return send_msg_card(error)


def send_create_msg(open_id):
    info = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "header": {
                "template": "green",
                "title": {
                    "tag": "plain_text",
                    "content": "初次见面！"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "欢迎来到封面生成助手，你可以把需要生成封面的图片和文字素材发送给我，我将智能生成合适排版的封面图~"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "○ 输入指令「1」后即可上传图片（上限为16张）\n"
                                   "○ 输入指令「2」后即可发送标题信息（7字以内，超出自动截取前7字）\n"
                                   "○ 输入指令「3」后即可发送副标题信息（11字以内，超出自动截取前11字）\n"
                                   "○ 输入指令「4」后即可执行渲染\n"
                                   "○ 输入指令「0」可终止整个流程（当输入信息有误时可用其复位）"
                    }
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": "※ 请在5分钟内完成上传，超时自动复位\n※ 在提交渲染处理之前，可随时新增图片\n※ 暂不支持繁体中文和其他生僻字符\n※ 暂不支持gif动图与部分冷门格式"
                        }
                    ]
                }
            ]
        }
    }

    # 发送提示
    return send_msg_card(info)


def send_repeat_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "请先完成当前任务后再创建新任务！"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_upload_pic_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "请开始上传你的图片（在5分钟内完成）~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_pic_count_msg(open_id, count):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "已上传" + str(count) + "张图片~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_first_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "请输入主标题（7字以内，超出自动截取前7字，在5分钟内完成）~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_secord_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "请输入副标题（11字以内，超出自动截取前11字，在5分钟内完成）~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_first_note_msg(open_id, first_title):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "确认主标题为「" + first_title + "」吗？如果需要修改可以直接输入，修改完后请输入「3」进入下一步~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_secord_note_msg(open_id, secord_title):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "确认副标题为「" + secord_title + "」吗？如果需要修改可以直接输入，修改完后可输入「2」修改主标题，或输入「4」执行渲染~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_out_of_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "已经超过16张图片上限啦！"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_check_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "请检查你的输入是否有遗漏！"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_over_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "生成次数已达到上限！请输入「0」复位，开始新的生成流程~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)

def send_unfill_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "请上传2张或以上的图片~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)

def send_wait_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "已收到指令，正在生成中~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_clear_msg(open_id):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "流程已清理完成~"
                    }
                }
            ]
        }
    }

    return send_msg_card(note)


def send_pic_msg(open_id, count, image_key):
    note = {
        "open_id": open_id,
        "msg_type": "interactive",
        'card': {
            "config": {
                "wide_screen_mode": False
            },
            "header": {
                "template": "green",
                "title": {
                    "tag": "plain_text",
                    "content": "生成结果"
                }
            },
            "elements": [
                {
                    'tag': 'img',
                    'img_key': image_key[0],
                    'alt': {
                        'tag': 'plain_text',
                        'content': '1'
                    }
                },
                {
                    'tag': 'img',
                    'img_key': image_key[1],
                    'alt': {
                        'tag': 'plain_text',
                        'content': '2'
                    }
                },
                {
                    'tag': 'img',
                    'img_key': image_key[2],
                    'alt': {
                        'tag': 'plain_text',
                        'content': '3'
                    }
                },
                {
                    'tag': 'div',
                    'text': {
                        'tag': 'plain_text',
                        'content': '本次生成结果如上，你还可生成' + str(count - 1) + '次（输入「4」继续生成）~'
                    },
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": "※ 5分钟后操作记录将清除，若需要再次生成需重新上传图片\n※ 若对当前结果满意，可直接输入「0」复位，开始新的生成流程"
                        }
                    ]
                }
            ]
        }
    }

    return send_msg_card(note)


def save_pic(record_id, open_id, pic_key, handler):
    access_token = get_tenant_access_token()

    if access_token is None:
        return "fail"

    # 创建文件夹并存入
    if not os.path.exists("cover_generator/" + str(record_id)):
        os.makedirs("cover_generator/" + str(record_id))
        os.makedirs("cover_generator/" + str(record_id) + "_temp")
        os.makedirs("cover_generator/" + str(record_id) + "_fin")

    # 当超过16张的时候直接返回（16张图片时提示无法继续输入）
    select_count_sql = "select record_pic_count from gen_pic where record_id = '%s'" % record_id
    rsg = handler.search_DB(select_count_sql)
    if rsg[0]["record_pic_count"] > 16:
        return send_out_of_msg(open_id)

    # 飞书API相关接口和交互参数
    search_pic_url = "https://open.feishu.cn/open-apis/image/v4/get?image_key=" + pic_key
    get_pic_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }
    try:

        # 从飞书服务器拉取用户发送的图片
        raw_pic = requests.get(search_pic_url, headers=get_pic_headers)
        pic_name = str(SnowId(1, 2, 0).get_id())[1:] + '.jpg'
        with open("cover_generator/" + str(record_id) + "/" + pic_name, 'wb') as fp:
            fp.write(raw_pic.content)

        # 把这个图片的后缀改为其真实的格式（飞书API的缺陷，无法确定真实格式，只能本地检测）
        real_rex = imghdr.what("cover_generator/" + str(record_id) + "/" + pic_name)
        if not real_rex:
            real_rex = "png"
        new_pic_name = os.path.splitext(pic_name)[0]
        search_pic_new_fullname = new_pic_name + '.' + real_rex
        os.rename("cover_generator/" + str(record_id) + "/" + pic_name, "cover_generator/" + str(record_id) + "/" + search_pic_new_fullname)

    except Exception as e:

        traceback.print_exc()
        print(e)
        return send_fail_msg(open_id, str(e) + traceback.format_exc())

    # 改变库中图片张数
    count_sql = "update gen_pic set record_pic_count=record_pic_count+'1' where record_id = '%s'" % record_id
    handler.modify_DB(count_sql)

    # 发送消息提示用户上传了几张图片
    send_pic_count_msg(open_id, rsg[0]["record_pic_count"] + 1)

    return "success"


def upload_pic(pic_path):
    with open(pic_path, 'rb') as f:
        image = f.read()
    upload_pic_url = 'https://open.feishu.cn/open-apis/image/v4/put/'
    access_token = get_tenant_access_token()
    upload_pic_headers = {
        "Authorization": "Bearer " + access_token
    }
    upload_pic_data = {
        "image_type": "message"
    }
    upload_pic_files = {
        "image": image
    }
    upload_pic_req = requests.post(url=upload_pic_url, headers=upload_pic_headers, files=upload_pic_files, data=upload_pic_data, stream=True)
    upload_pic_req.raise_for_status()
    receive_img_data = upload_pic_req.json()
    receive_img_key = receive_img_data["data"]["image_key"]
    # print(receive_img_key)
    return receive_img_key


app = Flask(__name__, static_folder='', static_url_path='')


@app.route('/', methods=['POST'])
def test():
    _data = json.loads(request.data)

    if "encrypt" in _data:
        cipher = AESCipher(APP_ENCRYPT_KEY)
        data = json.loads(cipher.decrypt_string(_data["encrypt"]))
    else:
        return "illegal"

    print(data)

    if "type" in data:
        msg_type = data["type"]
    else:
        return "illegal"

    # 校验 verification token 是否匹配，token 不匹配说明该回调并非来自开发平台
    if data["token"] != APP_VERIFICATION_TOKEN:
        print("verification token not match, token =", token)
        return "illegal"

    # 注册机器人验证
    if msg_type == "url_verification":
        rsg = {
            "challenge": data["challenge"]
        }
        return json.dumps(rsg)

    # 接下来主要处理会话事件，如果到这一步还没返回的，当做非法处理
    if "event" in data:
        event_data = data["event"]
    else:
        return "illegal"

    # type = p2p_chat_create 首次创建会话
    # type = message 对方发消息
    if "open_id" in event_data:
        open_id = event_data["open_id"]
    else:
        open_id = event_data["user"]["open_id"]

    # 首次进入bot会话，需要向当前用户介绍机器人的用法，以及提示用户先输入1开始流程
    if event_data["type"] == "p2p_chat_create":

        send_create_msg(open_id)
        return send_init_msg(open_id)

    # 如果输入的是普通文字或图片
    elif event_data["type"] == "message":

        # 其他类型的回复，仅回复提示
        if event_data["msg_type"] not in ["text", "image"]:
            print("unknown msg_type =", event_data)
            return send_tip_msg(open_id)

        db_handle = InstantDB().get_connect()

        # 如果输入为文字，进行文字相关的操作
        if event_data["msg_type"] == "text":

            if event_data["text"] == "1":

                try:
                    # 先查找5分钟内有没有
                    search_sql = "select * from gen_pic where record_created_by = '%s' " \
                                 "and record_created_at > DATE_SUB(NOW(), INTERVAL 5 MINUTE) " \
                                 "and record_status in ('1', '2', '3') limit 1" % \
                                 event_data["employee_id"]

                    if db_handle.search_DB(search_sql):
                        db_handle.db_close()
                        return send_repeat_msg(open_id)

                    # 没有记录，才创建新记录
                    record_created_by = event_data["employee_id"]
                    record_created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    create_sql = "INSERT INTO gen_pic(record_pic_count, record_created_by, record_created_at, record_status, record_changes) VALUES" \
                                 "('%s', '%s', '%s', '%s', '%s')" % \
                                 (0, record_created_by, record_created_at, "1", 5)
                    db_handle.modify_DB(create_sql)

                except Exception as e:

                    traceback.print_exc()
                    print(e)
                    db_handle.db_close()
                    return send_fail_msg(open_id, str(e) + traceback.format_exc())

                _return = send_upload_pic_msg(open_id)

            elif event_data["text"] == "2":

                # 没有创建得先创建
                search_sql = "select * from gen_pic where record_created_by = '%s' " \
                             "and record_created_at > DATE_SUB(NOW(), INTERVAL 5 MINUTE)" \
                             "and record_status in ('1', '2', '3') limit 1" % \
                             event_data["employee_id"]

                record = db_handle.search_DB(search_sql)

                if not record:
                    db_handle.db_close()
                    return send_init_msg(open_id)

                # 更新状态
                update_first_sql = "update gen_pic set record_status = '%s' where record_id = '%s'" % (2, record[0]["record_id"])
                db_handle.modify_DB(update_first_sql)

                return send_first_msg(open_id)

            elif event_data["text"] == "3":

                # 没有创建得先创建
                search_sql = "select * from gen_pic where record_created_by = '%s' " \
                             "and record_created_at > DATE_SUB(NOW(), INTERVAL 5 MINUTE)" \
                             "and record_status in ('1', '2', '3') limit 1" % \
                             event_data["employee_id"]

                record = db_handle.search_DB(search_sql)

                if not record:
                    db_handle.db_close()
                    return send_init_msg(open_id)

                # 更新状态
                update_secord_sql = "update gen_pic set record_status = '%s' where record_id = '%s'" % (3, record[0]["record_id"])
                db_handle.modify_DB(update_secord_sql)

                _return = send_secord_msg(open_id)

            elif event_data["text"] == "4":

                # 没有创建得先创建
                search_sql = "select * from gen_pic where record_created_by = '%s' " \
                             "and record_created_at > DATE_SUB(NOW(), INTERVAL 5 MINUTE)" \
                             "and record_status in ('2', '3') limit 1" % \
                             event_data["employee_id"]

                record = db_handle.search_DB(search_sql)

                # print(record)

                if not record:
                    db_handle.db_close()
                    return send_init_msg(open_id)

                # 检查各项信息是否为空，如果为空则提醒用户输入
                check_sql = "select * from gen_pic where record_created_by = '%s' " \
                            "and record_created_at > DATE_SUB(NOW(), INTERVAL 5 MINUTE)" \
                            "and record_pic_count != 0 " \
                            "and record_first_title is not null " \
                            "and record_secord_title is not null limit 1" % \
                            event_data["employee_id"]

                check = db_handle.search_DB(check_sql)

                if not check:
                    db_handle.db_close()
                    return send_check_msg(open_id)

                if check[0]["record_changes"] <= 0:
                    db_handle.db_close()
                    return send_over_msg(open_id)

                if check[0]["record_pic_count"] <= 1:
                    db_handle.db_close()
                    return send_unfill_msg(open_id)

                # 到这里说明要开始生成了，先发个消息让用户稍安勿躁
                send_wait_msg(open_id)

                # 调隔壁的函数进行渲染
                try:

                    image_list = Main().run(str(check[0]["record_id"]), check[0]["record_first_title"], check[0]["record_secord_title"])
                    image_key_list = []
                    for ikey in image_list:
                        image_key_list.append(upload_pic(ikey))
                        os.remove(ikey)

                    _return = send_pic_msg(open_id, check[0]["record_changes"], image_key_list)

                    # 改变生成次数
                    count_sql = "update gen_pic set record_changes=record_changes-'1' where record_id = '%s'" % check[0]["record_id"]
                    db_handle.modify_DB(count_sql)

                except Exception as e:

                    traceback.print_exc()
                    print(e)
                    db_handle.db_close()
                    return send_fail_msg(open_id, str(e) + traceback.format_exc())

            elif event_data["text"] == "0":

                # 没有创建得先创建
                search_sql = "select * from gen_pic where record_created_by = '%s' " \
                             "and record_created_at > DATE_SUB(NOW(), INTERVAL 5 MINUTE)" \
                             "and record_status in ('2', '3')" % \
                             event_data["employee_id"]

                record = db_handle.search_DB(search_sql)

                if not record:
                    db_handle.db_close()
                    return send_init_msg(open_id)

                # 清除当前用户的所有未完成的流程
                update_secord_sql = "update gen_pic set record_status = '%s' where record_status in ('1', '2', '3') and record_created_by = '%s'" % (5, event_data["employee_id"])
                db_handle.modify_DB(update_secord_sql)

                # 删除用户数据
                for ikey in record:
                    shutil.rmtree("cover_generator/" + str(ikey["record_id"]))
                    shutil.rmtree("cover_generator/" + str(ikey["record_id"]) + "_temp")
                    shutil.rmtree("cover_generator/" + str(ikey["record_id"]) + "_fin")

                _return = send_clear_msg(open_id)

            else:
                # 除非是状态2和状态3，其他的一律当乱输处理
                search_sql = "select * from gen_pic where record_created_by = '%s' " \
                             "and record_created_at > DATE_SUB(NOW(), INTERVAL 5 MINUTE)" \
                             "and record_status in ('2', '3') limit 1" % \
                             event_data["employee_id"]

                record = db_handle.search_DB(search_sql)

                if not record:

                    return send_tip_msg(open_id)

                else:

                    # 输入主标题
                    if record[0]["record_status"] == '2':

                        update_first_sql = "update gen_pic set record_first_title = '%s' where record_id = '%s'" % (event_data["text"][:7], record[0]["record_id"])
                        db_handle.modify_DB(update_first_sql)
                        _return = send_first_note_msg(open_id, event_data["text"][:7])


                    else:

                        update_secord_sql = "update gen_pic set record_secord_title = '%s' where record_id = '%s'" % (event_data["text"][:11], record[0]["record_id"])
                        db_handle.modify_DB(update_secord_sql)
                        _return = send_secord_note_msg(open_id, event_data["text"][:11])

        # 如果输入的是图片，首先查找当前用户是否在5分钟之内创建过记录，如果创建过就并入之前创建的记录，没有创建直接返回提示（先输入1开始流程）
        elif event_data["msg_type"] == "image":

            search_sql = "select * from gen_pic where record_created_by = '%s' " \
                         "and record_created_at > DATE_SUB(NOW(), INTERVAL 5 MINUTE)" \
                         "and record_status in ('1', '2', '3') limit 1" % \
                         event_data["employee_id"]

            record = db_handle.search_DB(search_sql)

            if not record:
                return send_init_msg(open_id)

            print(record[0]["record_id"])

            # 1 接收图片 2 把图片信息写入库
            _return = save_pic(record[0]["record_id"], open_id, event_data["image_key"], db_handle)

        else:
            return send_init_msg(open_id)

        db_handle.db_close()

        return _return

    return "success"


if __name__ == '__main__':
    app.debug = True
    server = pywsgi.WSGIServer(('0.0.0.0', 13105), application=app)
    print('web server started!')
    server.serve_forever()
