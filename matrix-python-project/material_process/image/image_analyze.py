import json, ssl, base64, requests, copy, os, traceback
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tiia.v20190529 import tiia_client, models
# ssl._create_default_https_context = ssl._create_unverified_context

class AnalyzeImage(object):

    def __init__(self):

        with open(os.getcwd() + "/material_process/layout.json", 'r') as f0:
            info = json.load(f0)

        self.azure_url = info["azure"]["url"]
        self.local_pic_url = info["azure"]["image_url"]
        self.analyze_json = {}
        self.auth = info["azure"]["auth"]
        self.app_id = info["tencent"]["app_id"]
        self.app_secret = info["tencent"]["app_secret"]
        self.area = info["tencent"]["area"]

    def tencent_pic(self, image_url_list):
        image_mark = 0
        tag_set = set()
        self.analyze_json["tencent_distinguish"] = []
        self.analyze_json["tencent_mark"] = []
        try:
            cred = credential.Credential(self.app_id, self.app_secret)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tiia.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tiia_client.TiiaClient(cred, self.area, clientProfile)

            req_1 = models.DetectLabelRequest()
            req_2 = models.AssessQualityRequest()

            for count, image_url in enumerate(image_url_list):
                with open(image_url + "_mini.jpg", 'rb') as f:
                    base64_data = base64.b64encode(f.read())
                    image_base64 = base64_data.decode()
                # 图片打标签
                params_1 = {
                    "Scenes": [ "CAMERA" ],
                    "ImageBase64": image_base64
                }
                req_1.from_json_string(json.dumps(params_1))
                resp_1 = client.DetectLabel(req_1)
                print(resp_1)
                if resp_1:
                    image_tag = json.loads(resp_1.to_json_string())
                    if image_tag["CameraLabels"]:
                        for ikey in image_tag["CameraLabels"]:
                            if ikey["Confidence"] >= 10:
                                tag_set.add(ikey["Name"])
                                tag_set.add(ikey["FirstCategory"])
                                tag_set.add(ikey["SecondCategory"])

                    self.analyze_json["tencent_distinguish"].append(image_tag)

                # 图片打分
                params_2 = {
                    "ImageBase64": image_base64
                }
                req_2.from_json_string(json.dumps(params_2))
                resp_2 = client.AssessQuality(req_2)
                print(resp_2)
                if resp_2:
                    image_mark_info = json.loads(resp_2.to_json_string())
                    if "AestheticScore" in image_mark_info and image_mark_info["AestheticScore"]:
                        image_mark += image_mark_info["AestheticScore"]
                    self.analyze_json["tencent_mark"].append(image_mark_info)

            # print(tag_set)
        except TencentCloudSDKException as err:
            print(err)
        return tag_set, round(image_mark, 2)

    def azure_pic(self, image_url_list):
        azure_tag_set = set()
        self.analyze_json["azure_distinguish"] = []
        headers = {
            'Ocp-Apim-Subscription-Key': self.auth,
            'Content-Type': 'application/json'
        }

        for count, image_url in enumerate(image_url_list):
            image_url_temp = image_url.split("/")[-1]
            data = {
                "url": self.local_pic_url + image_url_temp + "_mini.jpg"
            }
            try:
                assert self.auth and self.auth != ""
                response = requests.request("POST", self.azure_url, headers=headers, data=json.dumps(data), timeout=10)
                print(response.json())
                if response:
                    image_tag = response.json()
                    if image_tag["description"]["tags"]:
                        tag_length = len(image_tag["description"]["tags"])
                        if tag_length > 4:
                            tag_length = 4
                        for i in range(tag_length):
                            azure_tag_set.add(image_tag["description"]["tags"][i])
                    if image_tag["description"]["captions"]:
                        for sentence in image_tag["description"]["captions"]:
                            if sentence["confidence"] >= 0.1:
                                azure_tag_set.add(sentence["text"])

                    self.analyze_json["azure_distinguish"].append(image_tag)

            except Exception as e:
                traceback.print_exc()
                print(e)

        return azure_tag_set

    def tag_pic(self, image_url_list):
        all_tag_set = set()
        # 应该返回三个值：标签、打分、meta
        tag_temp, mark_temp = self.tencent_pic(image_url_list)
        image_tag = all_tag_set.union(tag_temp, self.azure_pic(image_url_list))
        return image_tag, mark_temp, self.analyze_json


# if __name__ == '__main__':
#     image_url_list = ["364037758150123520_cover", "364037758150123520_test"]
#     ai = AnalyzeImage()
#     print(ai.tag_pic(image_url_list))