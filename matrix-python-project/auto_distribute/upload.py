import sys, os, json, copy, random, time
sys.path.append(os.getcwd())
from db.db_pool_handler import InstantDBPool

class Upload(object):

    def __init__(self):

        with open("auto_distribute/distribute_config.json", 'r') as f0:
            self.info = json.load(f0)

        self.current_path = "auto_distribute/"

    def distribute(self, flow_id, keywords, adj_keywords):

        title_keywords = keywords[:3]
        random.shuffle(title_keywords)

        video_title = self.info["MANUSCRIPT_TITLE"].replace(
            "{{adj}}",
            adj_keywords[:2].split("/")
        ).replace(
            "{{noun}}",
            title_keywords.split("")
        )

        video_info = self.info["MANUSCRIPT_TITLE"].replace(
            "{{keywords}}",
            keywords.split("·")
        ).replace(
            "{{datetime}}",
            time.strftime('%Y.%m.%d', time.localtime())
        )

        # TODO 使用各类sdk完成上传操作

        print(self)


