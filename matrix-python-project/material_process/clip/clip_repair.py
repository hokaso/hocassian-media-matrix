"""
该方法用于修复部分未能成功打标签的视频素材
"""

import json, time, os, sys, requests, pymysql

sys.path.append(os.getcwd())

from db.database_handler import InstantDB
from material_process.clip.clip_analyze import ClipAnalyze


class ClipRepair(object):

    def __init__(self):
        # with open(os.getcwd() + "/material_process/config.json", 'r') as f0:
        #     # info = json.load(f0)
        #     info = json.load(f0)

        # self.__dict__ = {**self.__dict__, **info["local_prod"]}

        self.db_handle = InstantDB().get_connect()
        self.az = ClipAnalyze()

        current = os.getcwd().replace("/prod/matrix-python-project", "")
        self.clip_slot_path = current + "/matrix/material/video_clip/clip_slot/"

    def main(self):
        # 查数据库，看看哪些需要重新打标签

        prepare_sql = "SELECT material_id, material_path, material_tag from mat_clip where material_status = '0' limit 9000 offset 1000"

        all_prepared_clips = self.db_handle.search_DB(prepare_sql)

        for ikey in all_prepared_clips:

            # 查询该素材的tag是否够格
            material_tags = json.loads(ikey["material_tag"])

            if len(material_tags) < 2:

                # 将list_temp变成一个set
                set_temp = set(material_tags)
                image_url_list = [self.clip_slot_path + ikey["material_path"] + "_1"]

                # 需要重新过一遍处理
                image_tags, _, _, = self.az.tag_pic(image_url_list)

                for ukey in image_tags:
                    if ukey != "":
                        set_temp.add(ukey)

                list_temp = list(set_temp)
                print(set_temp)
                print(ikey["material_path"])

                rewrite_sql = "Update mat_clip set material_tag = '%s' where material_id = %s" % \
                              (pymysql.escape_string(json.dumps(list_temp, ensure_ascii=False)),
                               ikey["material_id"])

                self.db_handle.modify_DB(rewrite_sql)


if __name__ == '__main__':
    clip_repair = ClipRepair()
    clip_repair.main()
