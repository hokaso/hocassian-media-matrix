import sys, os, time, json, requests

sys.path.append(os.getcwd())
from utils.aes_cipher import AESCipher

with open("auto_distribute/lark_config.json", 'r') as f0:
    info = json.load(f0)

APP_ID = info["APP_ID"]
APP_SECRET = info["APP_SECRET"]
APP_VERIFICATION_TOKEN = info["APP_VERIFICATION_TOKEN"]
APP_ENCRYPT_KEY = info["APP_ENCRYPT_KEY"]
CURRENT_USER_OPENID = info["CURRENT_USER_OPENID"]


class Lark(object):

    def upload_pic(self, pic_path):
        with open(pic_path, 'rb') as f:
            image = f.read()
        upload_pic_url = 'https://open.feishu.cn/open-apis/image/v4/put/'
        access_token = self.get_tenant_access_token()
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

    @staticmethod
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

    def refresh_msg_card(self, body):
        url = 'https://open.feishu.cn/open-apis/interactive/v1/card/update'

        access_token = self.get_tenant_access_token()

        if access_token is None:
            return "fail"

        headers = {
            "Content-Type": "application/json; charset=utf-8",
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

    def send_msg_card(self, body):
        url = 'https://open.feishu.cn/open-apis/message/v4/send/'

        access_token = self.get_tenant_access_token()

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

    def send_starter_msg(self, duration, flow_id):
        note = {
            # 未来可以做成多租户模式
            "open_id": CURRENT_USER_OPENID,
            "msg_type": "interactive",
            'card': {
                "config": {
                    "wide_screen_mode": true
                },
                "header": {
                    "template": "wathet",
                    "title": {
                        "content": "素材量充足！需要分发视频嘛？",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "目前素材量总长度为：" + str(duration) + "s，是否需要分发？"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "分发视频"
                                },
                                "type": "primary",
                                "value": {
                                    "flow_type": "is_distributed",
                                    "flow_id": flow_id,
                                    "is_distributed": "1",
                                    "duration": duration
                                }
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "下次一定"
                                },
                                "type": "default",
                                "value": {
                                    "flow_type": "is_distributed",
                                    "flow_id": flow_id,
                                    "is_distributed": "0"
                                }
                            }
                        ]
                    }
                ]
            }
        }

        return self.send_msg_card(note)

    def send_cover_msg(self, cover_local_path, flow_id, thumbnail_list, keywords):

        pic_key = self.upload_pic(cover_local_path)
        note = {
            "open_id": CURRENT_USER_OPENID,
            "msg_type": "interactive",
            'card': {
                "config": {
                    "wide_screen_mode": true
                },
                "header": {
                    "template": "wathet",
                    "title": {
                        "content": "请选择是否采纳当前封面~",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "img",
                        "img_key": pic_key,
                        "alt": {
                            "tag": "plain_text",
                            "content": "封面图"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "就这张啦",
                                    "flow_type": "choose_cover",
                                    "flow_id": flow_id,
                                    "choose_cover": "1",
                                    "cover_pic": cover_local_path
                                },
                                "type": "primary"
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "换一张吧",
                                    "flow_type": "choose_cover",
                                    "flow_id": flow_id,
                                    "choose_cover": "0",
                                    "thumbnail_list": thumbnail_list,
                                    "keywords": keywords
                                },
                                "type": "danger"
                            }
                        ]
                    }
                ]
            }
        }

        return self.send_msg_card(note)

    def send_music_msg(self, duration, music_name, flow_id, music_url, audio_path):
        note = {
            # 未来可以做成多租户模式
            "open_id": CURRENT_USER_OPENID,
            "msg_type": "interactive",
            'card': {
                "config": {
                    "wide_screen_mode": true
                },
                "header": {
                    "template": "wathet",
                    "title": {
                        "content": "请选择是否采纳当前音乐~",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "当前音乐为：" + music_name + "，时长：" + str(duration) + "s"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "就这首啦",
                                    "flow_type": "choose_music",
                                    "flow_id": flow_id,
                                    "choose_music": "1",
                                    "audio_path": audio_path
                                },
                                "type": "primary"
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "试听一下"
                                },
                                "url": music_url,
                                "type": "default"
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "换一首吧",
                                    "flow_type": "choose_music",
                                    "flow_id": flow_id,
                                    "choose_music": "0",
                                    "count": 0
                                },
                                "type": "danger"
                            }
                        ]
                    }
                ]
            }
        }

        return self.send_msg_card(note)

    @staticmethod
    def send_music_refresh_msg(duration, music_name, flow_id, music_url, audio_path, count):
        note = {
            "config": {
                "wide_screen_mode": true
            },
            "header": {
                "template": "wathet",
                "title": {
                    "content": "请选择是否采纳当前音乐~",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "当前音乐为：" + music_name + "，时长：" + str(duration) + "s，重试次数：" + str(count)
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "就这首啦",
                                "flow_type": "choose_music",
                                "flow_id": flow_id,
                                "choose_music": "1",
                                "audio_path": audio_path
                            },
                            "type": "primary"
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "试听一下"
                            },
                            "url": music_url,
                            "type": "default"
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "换一首吧",
                                "flow_type": "choose_music",
                                "flow_id": flow_id,
                                "choose_music": "0",
                                "count": count + 1
                            },
                            "type": "danger"
                        }
                    ]
                }
            ]
        }

        return note

    def send_cover_refresh_msg(self, cover_local_path, flow_id, thumbnail_list, keywords, token, open_id):

        pic_key = self.upload_pic(cover_local_path)
        note = {
            "token": token,
            'card': {
                "open_ids":[open_id],
                "config": {
                    "wide_screen_mode": true
                },
                "header": {
                    "template": "wathet",
                    "title": {
                        "content": "请选择是否采纳当前封面~",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "img",
                        "img_key": pic_key,
                        "alt": {
                            "tag": "plain_text",
                            "content": "封面图"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "就这张啦",
                                    "flow_type": "choose_cover",
                                    "flow_id": flow_id,
                                    "choose_cover": "1",
                                    "cover_pic": cover_local_path
                                },
                                "type": "primary"
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "换一张吧",
                                    "flow_type": "choose_cover",
                                    "flow_id": flow_id,
                                    "choose_cover": "0",
                                    "thumbnail_list": thumbnail_list,
                                    "keywords": keywords
                                },
                                "type": "danger"
                            }
                        ]
                    }
                ]
            }
        }

        return self.refresh_msg_card(note)

    @staticmethod
    def send_continue_distribute_msg():
        note = {
            "config": {
                "wide_screen_mode": true
            },
            "header": {
                "template": "wathet",
                "title": {
                    "content": "当前封面已采纳",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "渲染&分发流程已启动，请等待程序自动执行完成~"
                    }
                }
            ]
        }

        return note

    @staticmethod
    def send_continue_music_msg():
        note = {
            "config": {
                "wide_screen_mode": true
            },
            "header": {
                "template": "wathet",
                "title": {
                    "content": "当前音乐已采纳",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "下面进入选择封面图环节~"
                    }
                }
            ]
        }

        return note

    @staticmethod
    def send_continue_msg():
        note = {
            "config": {
                "wide_screen_mode": true
            },
            "header": {
                "template": "wathet",
                "title": {
                    "content": "素材量充足！需要分发视频嘛？",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "请继续流程~"
                    }
                }
            ]
        }

        return note

    @staticmethod
    def send_cover_wait_msg():
        note = {
            "config": {
                "wide_screen_mode": true
            },
            "header": {
                "template": "wathet",
                "title": {
                    "content": "请选择是否采纳当前封面~",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "新的封面图生成中，请稍后……"
                    }
                }
            ]
        }

        return note

    @staticmethod
    def send_terminate_msg():
        note = {
            "config": {
                "wide_screen_mode": true
            },
            "header": {
                "template": "wathet",
                "title": {
                    "content": "素材量充足！需要分发视频嘛？",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "已选择跳过，那么下次一定哦~"
                    }
                }
            ]
        }

        return note
