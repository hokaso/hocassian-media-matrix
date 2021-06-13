import sys, os, time, json, requests, traceback
sys.path.append(os.getcwd())
from fake_useragent import UserAgent

class AudioAnalyze(object):

    def __init__(self):

        with open(os.getcwd() + "/material_process/config.json", 'r') as f0:
            info = json.loads(f0.read())

        self.ua = UserAgent()
        # 国内打标签
        self.emo_url = info["hifi"]["emo_url"]
        self.hifi_url = info["hifi"]["hifi_url"]
        self.hifi_url_token = info["hifi"]["hifi_url_token"]
        self.obtain_url = info["hifi"]["obtain_url"]
        self.payload = {}

    # 新文件名
    def run(self, audio_path):
        # 设置标签
        audio_set = set()
        analyze_json = {}

        try:
            # 上传到国内平台打标签
            files_class = {
                'file': (audio_path.split("/")[-1], open(audio_path, 'rb'), "audio/mp3")
            }
            files_emo = [('file', open(audio_path, 'rb'))]
            headers = {
                'Connection': 'keep-alive',
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
                'user-agent': self.ua.random
            }
            first_response = requests.request("POST", self.hifi_url, headers=headers, data=self.payload, files=files_class, timeout=10)
            first_data = first_response.json()
            analyze_json["hifi_raw"] = first_data
            time.sleep(10)
            second_response = requests.request("GET", self.obtain_url + first_data["data"]["fileKey"], headers=headers, data=self.payload, timeout=10)
            second_data = second_response.json()
            analyze_json["hifi_class"] = second_data
            for ikey in second_data["data"]["tags"]:
                audio_set.add(ikey["value"])

            emo_headers = {}
            emo_response = requests.request("POST", self.emo_url, headers=emo_headers, data=self.payload, files=files_emo, timeout=10)
            emo_data = emo_response.json()
            analyze_json["hifi_emo"] = emo_data
            for jkey in emo_data["result"]:
                audio_set.add(jkey["name"])

        except Exception as e:
            traceback.print_exc()
            print(e)

        return audio_set, analyze_json
