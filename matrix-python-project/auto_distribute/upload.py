import sys, os, json, random, time, shutil, traceback

sys.path.append(os.getcwd())
from youtube_upload import main
from bilibiliuploader.bilibiliuploader import BilibiliUploader
from bilibiliuploader.core import VideoPart
from db.db_pool_handler import InstantDBPool
from tenacity import retry, wait_random
from utils.snow_id import HSIS


WATCH_VIDEO_URL = "https://www.youtube.com/watch?v={id}"


class AuthenticationError(Exception): pass


class Options(object):

    def __init__(self):
        self.title = None
        self.description = None
        self.tags =None
        self.client_secrets =None
        self.credentials_file =None
        self.thumb =None
        self.category =None
        self.auth_browser = None
        self.publish_at = None
        self.title_template = "{title} [{n}/{total}]"
        self.privacy = "public"
        self.license = 'youtube'
        self.location = None
        self.recording_date = None
        self.default_audio_language = None
        self.default_language = None
        self.description_file = None
        self.playlist = None
        self.embeddable = True
        self.chunksize = 1024 * 1024 * 8


class Upload(object):

    def __init__(self):

        self.db_handle = InstantDBPool().get_connect()

        with open("auto_distribute/config/distribute_config.json", 'r') as f0:
            self.info = json.load(f0)

        self.bilibili_token_file_path = "auto_distribute/config/bilibili_config.json"
        self.current_path = "auto_distribute/"
        self.ytb_current_path = os.getcwd() + "/auto_distribute/"
        self.store_path = os.getcwd().replace("/prod/matrix-python-project", "") + "/matrix/distribute/"

        self.video_path = ""
        self.pic_path = ""
        self.video_title = ""
        self.video_info = ""
        self.video_tags = []

    def distribute(self, flow_id, keywords, adj_keywords):

        random.shuffle(keywords)
        title_keywords = keywords[:3]

        self.video_title = self.info["MANUSCRIPT_TITLE"].replace(
            "{{adj}}",
            "/".join(adj_keywords[:2])
        ).replace(
            "{{noun}}",
            "".join(title_keywords)
        )

        self.video_info = self.info["MANUSCRIPT_INFO"].replace(
            "{{keywords}}",
            "·".join(keywords)
        ).replace(
            "{{datetime}}",
            time.strftime('%Y.%m.%d', time.localtime())
        )

        self.video_path = self.current_path + str(flow_id) + "_output.mp4"
        self.pic_path = self.current_path + str(flow_id) + "_cover.jpg"
        self.video_tags = self.info["EXTRA_TAGS"] + keywords

        try:

            # 完成bilibili上传
            bilibili_id = self.bilibili_upload()

            # 完成YouTube上传
            youtube_id = self.youtube_upload()

            # 修改流程表记录
            finish_flow_sql = "update flow_distribute set youtube_id = '%s', bilibili_id = '%s', status = '%s' where id = '%s' and status = '%s'" % \
                              (youtube_id, bilibili_id, "5", flow_id, "4")

            self.db_handle.modify(finish_flow_sql)

        except Exception as e:
            print(e)
            traceback.print_exc()
            return

        ytb_url = WATCH_VIDEO_URL.format(id=youtube_id)
        return self.video_title, self.video_info, ytb_url

    @retry(wait=wait_random(min=360, max=720))
    def youtube_upload(self):

        # 设置环境变量
        os.environ['http_proxy'] = self.info["YOUTUBE_HTTP_PROXY"]
        os.environ['https_proxy'] = self.info["YOUTUBE_HTTPS_PROXY"]

        options = Options()
        # setattr(options, 'title', self.video_title)
        # setattr(options, 'description', self.video_info)
        # setattr(options, 'tags', ",".join(self.video_tags))
        # setattr(options, 'client_secrets', self.current_path + "config/client_secret.json")
        # setattr(options, 'credentials_file', self.current_path + "config/credentials_file.json")
        # setattr(options, 'thumb', self.pic_path)
        # setattr(options, 'category', self.info["YOUTUBE_CATEGORY"])
        # setattr(options, 'title', self.video_title)

        options.title = self.video_title
        options.description = self.video_info
        options.tags = ",".join(self.video_tags)
        options.client_secrets = self.ytb_current_path + "config/client_secret.json"
        options.credentials_file = self.ytb_current_path + "config/credentials_file.json"
        options.thumb = self.pic_path
        options.category = self.info["YOUTUBE_CATEGORY"]

        youtube = main.get_youtube_handler(options)

        if youtube:

            video_id = main.upload_youtube_video(youtube, options, self.video_path, 0, 0)
            video_url = WATCH_VIDEO_URL.format(id=video_id)
            # debug("Video URL: {0}".format(video_url))

            if options.thumb:
                youtube.thumbnails().set(videoId=video_id, media_body=options.thumb).execute()

            print(video_url + "\n")
        else:
            raise AuthenticationError("Cannot get youtube resource")

        # 改回环境变量
        os.environ['http_proxy'] = ""
        os.environ['https_proxy'] = ""

        return video_id

    @retry(wait=wait_random(min=360, max=720))
    def bilibili_upload(self):

        uploader = BilibiliUploader()

        # 登录
        try:
            uploader.login_by_access_token_file(self.bilibili_token_file_path)
        except Exception as e:
            print(e)
            traceback.print_exc()
            try:
                uploader.login(self.info["BILIBILI_ACCOUNT"], self.info["BILIBILI_SECRET"])
            except Exception as e:
                print(e)
                traceback.print_exc()
                # 到这里要是再出错，神仙也救不了……
                uploader.login(self.info["BILIBILI_ACCOUNT"], self.info["BILIBILI_SECRET"])

            finally:
                uploader.save_login_data(file_name=self.bilibili_token_file_path)

        try:

            # 处理视频文件
            parts = [VideoPart(
                path=self.video_path,
                title=self.video_title,
                desc=self.video_info
            )]

            # 上传
            avid, bvid = uploader.upload(
                parts=parts,
                copyright=1,
                title=self.video_title,
                tid=self.info["BILIBILI_CATEGORY"],
                tag=",".join(self.video_tags[:9]),
                desc=self.video_info,
                cover=self.pic_path
            )

        except Exception as e:
            print(e)
            traceback.print_exc()
            return

        return str(avid) + "-" + str(bvid)

    def fix_records(self, flow_id, keywords, adj_keywords):

        select_current_flow_detail_sql = "SELECT status, mat_list, audio_path, cover_pic, keywords, adj_keywords FROM flow_distribute " \
                                         "WHERE id = '%s' LIMIT 1" % flow_id
        _current_flow_detail = self.db_handle.search(select_current_flow_detail_sql)
        current_flow_detail = _current_flow_detail[0]

        mat_list = json.loads(current_flow_detail["mat_list"])

        random.shuffle(keywords)
        title_keywords = keywords[:3]

        self.video_title = self.info["MANUSCRIPT_TITLE"].replace(
            "{{adj}}",
            "/".join(adj_keywords[:2])
        ).replace(
            "{{noun}}",
            "".join(title_keywords)
        )

        self.video_info = self.info["MANUSCRIPT_INFO"].replace(
            "{{keywords}}",
            "·".join(keywords)
        ).replace(
            "{{datetime}}",
            time.strftime('%Y.%m.%d', time.localtime())
        )

        # 这个方法专门用于修复上传失败的流程
        after_name = HSIS.main()
        shutil.copyfile(self.current_path + str(flow_id) + "_output.mp4", self.store_path + after_name + ".mp4")
        shutil.copyfile(self.current_path + str(flow_id) + "_cover.jpg", self.store_path + after_name + ".jpg")

        with open(self.store_path + after_name + ".txt", "w+") as temp_txt_file:
            temp_txt_file.writelines(self.video_title + "\n")
            temp_txt_file.writelines(self.video_info + "\n")
            temp_txt_file.writelines(current_flow_detail["keywords"] + "\n")
            temp_txt_file.writelines(current_flow_detail["adj_keywords"] + "\n")

        # 更新素材表记录，证明相关素材已经被分发，下次无需分发
        mat_id_list = [m["material_id"] for m in mat_list]
        update_mat_clip_sql = "update mat_clip set has_uploaded = '%s' where material_id in (%s)" % ("1", ','.join(['%s'] * (len(mat_id_list))))
        # print(update_mat_clip_sql)
        self.db_handle.modify(update_mat_clip_sql, mat_id_list)


if __name__ == '__main__':
    a = 22
    b = ["场景", "建筑", "户外", "人", "人体", "男人", "室内", "", "物品", "人物"]
    c = ["可商用", "10bit", "HLG"]
    up = Upload()
    up.distribute(a, b, c)
    up.fix_records(a, b, c)

