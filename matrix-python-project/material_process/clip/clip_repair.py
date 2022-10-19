"""
该方法用于修复部分未能成功打标签的视频素材
"""

import json, time, os, sys, requests, pymysql

sys.path.append(os.getcwd())

from db.db_pool_handler import InstantDBPool
from material_process.clip.clip_analyze import ClipAnalyze


class ClipRepair(object):

    def __init__(self):
        # with open(os.getcwd() + "/material_process/config.json", 'r') as f0:
        #     # info = json.load(f0)
        #     info = json.load(f0)

        # self.__dict__ = {**self.__dict__, **info["local_prod"]}

        self.db_handle = InstantDBPool().get_connect()
        self.az = ClipAnalyze()

        current = os.getcwd().replace("/prod/matrix-python-project", "")
        self.clip_slot_path = current + "/matrix/material/video_clip/clip_slot/"

    def main(self):
        # 查数据库，看看哪些需要重新打标签

        prepare_sql = "SELECT material_id, material_path, material_tag from mat_clip where material_status = '0' order by material_id desc limit 100"

        all_prepared_clips = self.db_handle.search(prepare_sql)

        for ikey in all_prepared_clips:

            # 查询该素材的tag是否够格
            material_tags = json.loads(ikey["material_tag"])

            if len(material_tags) < 10:

                # 将list_temp变成一个set
                set_temp = set(material_tags)
                image_url_list = [self.clip_slot_path + ikey["material_path"] + "_1"]

                # 需要重新过一遍处理
                image_tags, _, _, = self.az.tag_pic(image_url_list)
                for jkey in image_tags:
                    set_temp.add(jkey)

                print(set_temp)
                print(ikey["material_path"])

                rewrite_sql = "Update mat_clip set material_tag = '%s' where material_id = %s" % \
                              (pymysql.converters.escape_string(json.dumps(list(set_temp), ensure_ascii=False)),
                               ikey["material_id"])

                self.db_handle.modify(rewrite_sql)


if __name__ == '__main__':
    clip_repair = ClipRepair()
    clip_repair.main()
