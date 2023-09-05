from yt_dlp import YoutubeDL
import os, sys

sys.path.append(os.getcwd())
from db.db_pool_handler import InstantDBPool
from PIL import Image
from utils.snow_id import HSIS
from tenacity import retry, wait_random
import json, pymysql, time, traceback, shutil
import emoji


class VideoDownload(object):

    def __init__(self):
        self.db_handle = InstantDBPool().get_connect()

        with open(os.getcwd() + "/sync_ytb_video/config.json", 'r') as f0:
            info = json.load(f0)

        self.ydl_opts = {
            'writesubtitles': True,
            'subtitlesformat': 'vtt',
            'ignoreerrors': True,
            'writethumbnail': True,
            'writeinfojson': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
            'recode_video': 'mp4',
            'merge_output_format': 'mp4',
            'nocheckcertificate': True,
            "proxy": info["ydl_opts"]["proxy"],
            "outtmpl": info["ydl_opts"]["outtmpl"],
            "cookies": info["ydl_opts"]["cookies"],
            "--skip-download": ""
        }

        self.file_path = info["file_path"]
        self.file_path_temp = info["file_path"] + "temp/"
        if not os.path.exists(self.file_path_temp):
            os.makedirs(self.file_path_temp)

    def run(self):

        # os.system("sudo pip3 install --upgrade youtube-dl")
        os.system("sudo pip3 install --upgrade yt_dlp")

        uncatch_channel_sql = "SELECT channel_id, channel_url from bus_channel"

        uncatch_channel = self.db_handle.search(uncatch_channel_sql)

        try:

            for j in uncatch_channel:

                # sql_map = {}
                select_all_sql = "SELECT video_ytb_id, video_status from bus_video where video_author = '%s'" % str(
                    j["channel_id"])
                all_video = self.db_handle.search(select_all_sql)
                if all_video:
                    all_video_list = [i["video_ytb_id"] for i in all_video]

                else:
                    all_video_list = []

                ydl = YoutubeDL(self.ydl_opts)
                ydl.add_default_info_extractors()
                info = ydl.extract_info(j["channel_url"], download=False)

                # 测试使用
                with open("full_info.json", 'w') as fp:
                    json.dump(info, fp)
                with open("full_info.json", 'r') as f0:
                    info = json.load(f0)

                for i in info["entries"]:

                    if i:
                        if "id" in i:
                            if i["id"] not in all_video_list:
                                video_status = "2"
                            else:
                                video_status = "-1"

                            video_ytb_id = pymysql.converters.escape_string(i["id"])
                        else:
                            continue
                    else:
                        continue
                    if "webpage_url" in i:
                        video_url = pymysql.converters.escape_string(i["webpage_url"])
                    else:
                        continue
                    if "title" in i:
                        video_title = emoji.demojize(pymysql.converters.escape_string(i["title"]))
                    else:
                        video_title = ""
                    if "description" in i:
                        video_profile = emoji.demojize(pymysql.converters.escape_string(i["description"]))
                    else:
                        video_profile = ""
                    if "upload_date" in i:
                        timeArray = time.strptime(i["upload_date"], "%Y%m%d")
                        video_publish = time.strftime("%Y-%m-%d", timeArray)
                    else:
                        video_publish = "1970-01-02"

                    video_class = ""
                    if "categories" in i and "tags" in i:
                        if i["categories"] is not None and i["tags"] is not None:
                            _video_class = i["categories"] + i["tags"]
                            video_class = pymysql.converters.escape_string(json.dumps(_video_class, ensure_ascii=False))
                        elif i["categories"] is None and i["tags"] is not None:
                            _video_class = i["tags"]
                            video_class = pymysql.converters.escape_string(json.dumps(_video_class, ensure_ascii=False))
                        elif i["categories"] is not None and i["tags"] is None:
                            _video_class = i["categories"]
                            video_class = pymysql.converters.escape_string(json.dumps(_video_class, ensure_ascii=False))

                    if video_status == "2":

                        insert_video_sql = "INSERT INTO bus_video(video_ytb_id ,video_title, video_profile, video_url," \
                                           " video_status, video_class, video_author, video_publish) VALUES " \
                                           "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                           (video_ytb_id, video_title, video_profile, video_url, video_status, video_class,
                                            str(j["channel_id"]), video_publish)

                        self.db_handle.modify(insert_video_sql)

                    else:
                        update_video_sql = "UPDATE bus_video set video_title = '%s', video_profile = '%s', video_url = '%s'," \
                                           " video_class = '%s', video_author = '%s', video_publish = '%s' where video_ytb_id = '%s'" % \
                                           (video_title, video_profile, video_url, video_class, str(j["channel_id"]),
                                            video_publish, video_ytb_id)

                        self.db_handle.modify(update_video_sql)

        except Exception as e:
            traceback.print_exc()
            print(e)

        self.video_dl()

    # 把建立视频索引和下载视频的操作进行隔离，确保即便当前cron job出错，下一个生命周期也能兜底
    @retry(wait=wait_random(min=3600, max=7200))
    def video_dl(self):

        try:

            ydlk = YoutubeDL(self.ydl_opts)
            ydlk.add_default_info_extractors()
            dl_sql = "select video_ytb_id, video_url from bus_video where video_pic IS NULL or video_pic ='' ORDER BY RAND()"
            dl_url = self.db_handle.search(dl_sql)

            for t in dl_url:
                ydlk.extract_info(t["video_url"], download=True)
                after_name = HSIS.main()

                # 重命名视频
                os.rename(self.file_path_temp + t["video_ytb_id"] + ".mp4", self.file_path_temp + after_name + ".mp4")
                os.rename(self.file_path_temp + t["video_ytb_id"] + ".info.json", self.file_path_temp + after_name + ".json")

                # 重命名图片
                if os.path.isfile(self.file_path_temp + t["video_ytb_id"] + ".jpg"):
                    os.rename(self.file_path_temp + t["video_ytb_id"] + ".jpg", self.file_path_temp + after_name + ".jpg")
                elif os.path.isfile(self.file_path_temp + t["video_ytb_id"] + ".webp"):
                    target = Image.open(self.file_path_temp + t["video_ytb_id"] + ".webp")
                    target = target.convert('RGB')
                    target.save(self.file_path_temp + after_name + ".jpg", quality=100)
                    os.remove(self.file_path_temp + t["video_ytb_id"] + ".webp")
                elif os.path.isfile(self.file_path_temp + t["video_ytb_id"] + ".png"):
                    target = Image.open(self.file_path_temp + t["video_ytb_id"] + ".png")
                    target = target.convert('RGB')
                    target.save(self.file_path_temp + after_name + ".jpg", quality=100)
                    os.remove(self.file_path_temp + t["video_ytb_id"] + ".png")
                else:
                    after_name = "undefined"

                # 如有字幕，重命名字幕
                has_sub = "0"
                sub_list = []
                for root, dirs, files in os.walk(self.file_path_temp):
                    # 遍历所有文件
                    for file in files:
                        if file.endswith('.vtt'):
                            has_sub = "1"
                            sub_name = file.split(".")
                            # 下表为1的值表示字幕语言（例如：zh-Hant）
                            if sub_name[1] == "vtt":
                                # 表示默认语言，直接vtt即可
                                os.rename(self.file_path_temp + file, self.file_path_temp + after_name + ".vtt")
                            else:
                                sub_list.append(sub_name[1])
                                os.rename(self.file_path_temp + file, self.file_path_temp + after_name + "-" + sub_name[1] + ".vtt")

                if sub_list:
                    sub_list_fin = pymysql.converters.escape_string(json.dumps(sub_list, ensure_ascii=False))
                else:
                    sub_list_fin = ""

                # 把所有文件移动到主文件夹下
                temp_files = os.listdir(self.file_path_temp)
                for file in temp_files:
                    shutil.copy(self.file_path_temp + file, self.file_path)
                    os.remove(self.file_path_temp + file)

                update_video_sql = "update bus_video set video_path = '%s', video_json = '%s', video_pic = '%s', video_status = '%s', video_is_huge = '%s', video_has_subtitle = '%s', video_sub_list = '%s' where video_ytb_id = '%s'" % \
                                   (after_name + ".mp4", after_name + ".json", after_name + ".jpg", "0", "1", has_sub, sub_list_fin, t["video_ytb_id"])
                self.db_handle.modify(update_video_sql)

        except Exception as e:
            traceback.print_exc()
            print(e)


if __name__ == '__main__':
    video_download = VideoDownload()
    video_download.run()
    # video_download.video_dl()
