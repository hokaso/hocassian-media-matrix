import sys, os, json, requests

sys.path.append(os.getcwd())


class Lark(object):

    def __init__(self):
        with open("auto_distribute/config/lark_config.json", 'r') as f0:
            info = json.load(f0)

        self.app_id = info["APP_ID"]
        self.app_secret = info["APP_SECRET"]
        self.app_verification_token = info["APP_VERIFICATION_TOKEN"]
        self.app_encrypt_key = info["APP_ENCRYPT_KEY"]
        self.current_user_openid = info["CURRENT_USER_OPENID"]

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

    def get_tenant_access_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"

        headers = {
            "Content-Type": "application/json"
        }

        body = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
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
            print(e)
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
            print(e)
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
            "open_id": self.current_user_openid,
            "msg_type": "interactive",
            'card': {
                "config": {
                    "wide_screen_mode": True
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

        print(note)

        return self.send_msg_card(note)

    def send_cover_msg(self, cover_local_path, flow_id, thumbnail_list, keywords):

        pic_key = self.upload_pic(cover_local_path)
        note = {
            "open_id": self.current_user_openid,
            "msg_type": "interactive",
            'card': {
                "config": {
                    "wide_screen_mode": True
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
                                    "content": "就这张啦"
                                },
                                "type": "primary",
                                "value": {
                                    "flow_type": "choose_cover",
                                    "flow_id": flow_id,
                                    "choose_cover": "1",
                                    "cover_pic": cover_local_path
                                }
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "换一张吧"
                                },
                                "type": "danger",
                                "value": {
                                    "flow_type": "choose_cover",
                                    "flow_id": flow_id,
                                    "choose_cover": "0",
                                    "thumbnail_list": thumbnail_list,
                                    "keywords": keywords
                                }
                            }
                        ]
                    }
                ]
            }
        }

        return self.send_msg_card(note)

    def send_music_msg(self, duration, music_name, flow_id, music_url, audio_path, mat_duration):
        note = {
            # 未来可以做成多租户模式
            "open_id": self.current_user_openid,
            "msg_type": "interactive",
            'card': {
                "config": {
                    "wide_screen_mode": True
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
                                    "content": "就这首啦"
                                },
                                "value": {
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
                                "url": music_url + ".mp3",
                                "type": "default"
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "换一首吧"
                                },
                                "value": {
                                    "flow_type": "choose_music",
                                    "flow_id": flow_id,
                                    "choose_music": "0",
                                    "count": 0,
                                    "duration": mat_duration
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
    def send_music_refresh_msg(duration, music_name, flow_id, music_url, audio_path, count, mat_duration):
        note = {
            "config": {
                "wide_screen_mode": True
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
                                "content": "就这首啦"
                            },
                            "value": {
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
                            "url": music_url + ".mp3",
                            "type": "default"
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "换一首吧"
                            },
                            "value": {
                                "flow_type": "choose_music",
                                "flow_id": flow_id,
                                "choose_music": "0",
                                "count": count + 1,
                                "duration": mat_duration
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
                "open_ids": [open_id],
                "config": {
                    "wide_screen_mode": True
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
                                    "content": "就这张啦"
                                },
                                "value": {
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
                                    "content": "换一张吧"
                                },
                                "value": {
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
                "wide_screen_mode": True
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
                "wide_screen_mode": True
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
                "wide_screen_mode": True
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
                "wide_screen_mode": True
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
                "wide_screen_mode": True
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

    def send_create_msg(self):
        note = {
            "open_id": self.current_user_openid,
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
                            "content": "欢迎来到素材分发助手~"
                        }
                    }
                ]
            }
        }

        # 发送提示
        return self.send_msg_card(note)

    def send_finish_msg(self, video_title, ytb_url):

        note = {
            "open_id": self.current_user_openid,
            "msg_type": "interactive",
            'card': {
                "config": {
                    "wide_screen_mode": False
                },
                "header": {
                    "template": "green",
                    "title": {
                        "tag": "plain_text",
                        "content": "分发完成~"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "plain_text",
                            "content": "视频标题：" + video_title
                        }
                    },
                    {
                        "tag": "markdown",
                        "content": "油管链接：[点我查看]("+ ytb_url +")"
                    }
                ]
            }
        }

        # 发送提示
        return self.send_msg_card(note)

    def send_mat_not_enough(self):

        note = {
            "open_id": self.current_user_openid,
            "msg_type": "interactive",
            'card': {
                "config": {
                    "wide_screen_mode": False
                },
                "header": {
                    "template": "orange",
                    "title": {
                        "tag": "plain_text",
                        "content": "素材不足T_T"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "plain_text",
                            "content": "素材不够分发啦，还请大佬再接再厉~"
                        }
                    }
                ]
            }
        }

        # 发送提示
        return self.send_msg_card(note)