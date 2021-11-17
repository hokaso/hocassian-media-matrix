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

    def send_cover_msg(self):

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
                        "img_key": "",
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
                                    "content": "就这张啦"
                                },
                                "type": "primary"
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "换一张吧"
                                },
                                "type": "danger"
                            }
                        ]
                    }
                ]
            }
        }

        return self.send_msg_card(note)

    def send_music_msg(self, duration, music_name, flow_id, music_url, music_id):
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
                                    "music_id": music_id
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
    def send_music_refresh_msg(duration, music_name, flow_id, music_url, music_id, count):
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
                                "music_id": music_id
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

    @staticmethod
    def send_music_continue_msg():
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
                        "content": "渲染&分发流程已启动，请等待程序自动执行完成~"
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
