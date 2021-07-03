import schedule, time, sys, os, shutil
sys.path.append(os.getcwd())

from db.database_handler import InstantDB


class Operator(object):

    def __init__(self):
        self.db_handle = InstantDB().get_connect()

    def main(self):

        # 每天清除一次
        pick_sql = "select record_id from gen_pic where record_status in ('1', '2', '3') and record_created_at < DATE_SUB(NOW(), INTERVAL 1 DAY)"
        rsg = self.db_handle.search_DB(pick_sql)
        id_list = [i["record_id"] for i in rsg]

        print(id_list)

        # 删除用户数据
        for ikey in id_list:

            try:
                shutil.rmtree("cover_generator/" + str(ikey))
                shutil.rmtree("cover_generator/" + str(ikey) + "_temp")
                shutil.rmtree("cover_generator/" + str(ikey) + "_fin")
            except Exception as e:
                print(e)

            update_sql = "update gen_pic set record_status = '4' where record_id = '%s'" % ikey
            self.db_handle.modify_DB(update_sql)

if __name__ == '__main__':
    p = Operator().main
    schedule.every(1).days.at("04:00").do(p)
    print("脚本已启动")
    while True:
        schedule.run_pending()
        time.sleep(1)

# if __name__ == '__main__':
#     Operator().main()