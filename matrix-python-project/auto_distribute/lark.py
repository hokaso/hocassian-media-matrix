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
            # ?????????????????????????????????
            "open_id": self.current_user_openid,
            "msg_type": "interactive",
            'card': {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "template": "wathet",
                    "title": {
                        "content": "??????????????????????????????????????????",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "??????????????????????????????" + str(duration) + "s????????????????????????"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "????????????"
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
                                    "content": "????????????"
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
                        "content": "?????????????????????????????????~",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "img",
                        "img_key": pic_key,
                        "alt": {
                            "tag": "plain_text",
                            "content": "?????????"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "????????????"
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
                                    "content": "????????????"
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
            # ?????????????????????????????????
            "open_id": self.current_user_openid,
            "msg_type": "interactive",
            'card': {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "template": "wathet",
                    "title": {
                        "content": "?????????????????????????????????~",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "??????????????????" + music_name + "????????????" + str(duration) + "s"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "????????????"
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
                                    "content": "????????????"
                                },
                                "url": music_url + ".mp3",
                                "type": "default"
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "????????????"
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
                    "content": "?????????????????????????????????~",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "??????????????????" + music_name + "????????????" + str(duration) + "s??????????????????" + str(count)
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "????????????"
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
                                "content": "????????????"
                            },
                            "url": music_url + ".mp3",
                            "type": "default"
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "????????????"
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
                        "content": "?????????????????????????????????~",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "img",
                        "img_key": pic_key,
                        "alt": {
                            "tag": "plain_text",
                            "content": "?????????"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "????????????"
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
                                    "content": "????????????"
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
                    "content": "?????????????????????",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "??????&?????????????????????????????????????????????????????????~"
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
                    "content": "?????????????????????",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "?????????????????????????????????~"
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
                    "content": "??????????????????????????????????????????",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "???????????????~"
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
                    "content": "?????????????????????????????????~",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "??????????????????????????????????????????"
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
                    "content": "??????????????????????????????????????????",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "???????????????????????????????????????~"
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
                        "content": "???????????????"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "plain_text",
                            "content": "??????????????????????????????~"
                        }
                    }
                ]
            }
        }

        # ????????????
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
                        "content": "????????????~"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "plain_text",
                            "content": "???????????????" + video_title
                        }
                    },
                    {
                        "tag": "markdown",
                        "content": "???????????????[????????????]("+ ytb_url +")"
                    }
                ]
            }
        }

        # ????????????
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
                        "content": "????????????T_T"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "plain_text",
                            "content": "????????????????????????????????????????????????~"
                        }
                    }
                ]
            }
        }

        # ????????????
        return self.send_msg_card(note)