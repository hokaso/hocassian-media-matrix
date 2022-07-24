"""
该方法用于修复部分未能成功打标签的图片素材
"""

import json, time, os, sys, requests, pymysql

sys.path.append(os.getcwd())

from db.database_handler import InstantDB
from material_process.image.image_analyze import AnalyzeImage


class ClipRepair(object):

    def __init__(self):
        # with open(os.getcwd() + "/image_process/config.json", 'r') as f0:
        #     # info = json.load(f0)
        #     info = json.load(f0)

        # self.__dict__ = {**self.__dict__, **info["local_prod"]}

        self.db_handle = InstantDB().get_connect()
        self.az = AnalyzeImage()

        current = os.getcwd().replace("/prod/matrix-python-project", "")
        self.final_path = current + "/matrix/material/image/"

    def main(self):
        # 查数据库，看看哪些需要重新打标签

        prepare_sql = "SELECT image_id, image_path, image_tag from mat_image where image_status = '0'"

        all_prepared_images = self.db_handle.search_DB(prepare_sql)

        for ikey in all_prepared_images:

            # 查询该素材的tag是否够格
            image_tags = json.loads(ikey["image_tag"])

            if len(image_tags) < 6:

                # 将list_temp变成一个set
                set_temp = set(image_tags)
                image_url_list = [self.final_path + ikey["image_path"]]

                # 需要重新过一遍处理
                image_tags, _, _, = self.az.tag_pic(image_url_list)

                for jkey in image_tags:
                    set_temp.add(jkey)

                list_temp = list(set_temp)

                print(image_tags)
                print(ikey["image_path"])

                rewrite_sql = "Update mat_image set image_tag = '%s' where image_id = %s" % \
                              (pymysql.escape_string(json.dumps(list_temp, ensure_ascii=False)),
                               ikey["image_id"])

                self.db_handle.modify_DB(rewrite_sql)


if __name__ == '__main__':
    clip_repair = ClipRepair()
    clip_repair.main()
