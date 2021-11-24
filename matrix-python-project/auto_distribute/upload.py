import sys, os, json, copy, random, time

sys.path.append(os.getcwd())
from db.db_pool_handler import InstantDBPool
from youtube_upload import main
from bilibiliuploader.bilibiliuploader import BilibiliUploader
from bilibiliuploader.core import VideoPart

WATCH_VIDEO_URL = "https://www.youtube.com/watch?v={id}"


class AuthenticationError(Exception): pass


class Options(object): pass


class Upload(object):

    def __init__(self):

        with open("auto_distribute/distribute_config.json", 'r') as f0:
            self.info = json.load(f0)

        self.current_path = "auto_distribute/"

        self.video_path = ""
        self.pic_path = ""
        self.video_title = ""
        self.video_info = ""
        self.video_tags = []

    def distribute(self, flow_id, keywords, adj_keywords):

        title_keywords = keywords[:3]
        random.shuffle(title_keywords)

        self.video_title = self.info["MANUSCRIPT_TITLE"].replace(
            "{{adj}}",
            "/".join(adj_keywords[:2])
        ).replace(
            "{{noun}}",
            "".join(title_keywords)
        )

        self.video_info = self.info["MANUSCRIPT_TITLE"].replace(
            "{{keywords}}",
            "·".join(keywords)
        ).replace(
            "{{datetime}}",
            time.strftime('%Y.%m.%d', time.localtime())
        )

        self.video_path = self.current_path + str(flow_id) + "_output.mp4"
        self.pic_path = self.current_path + str(flow_id) + "_cover.jpg"
        self.video_tags = self.info["EXTRA_TAGS"] + keywords

        # 完成bilibili上传
        bilibili_id = self.bilibili_upload()

        # 完成YouTube上传
        youtube_id = self.youtube_upload()

        # 修改流程表记录
        finish_flow_sql = "update flow_distribute set youtube_id = '%s', bilibili_id = '%s', status = '%s' where id = '%s' and status = '%s'" % \
                          (youtube_id, bilibili_id, "5", flow_id, "4")

        self.db_handle.modify(finish_flow_sql)
        return self.video_title, self.video_info

    def youtube_upload(self):

        # 设置环境变量
        os.environ['http_proxy'] = self.info["YOUTUBE_HTTP_PROXY"]
        os.environ['https_proxy'] = self.info["YOUTUBE_HTTPS_PROXY"]

        options = Options()
        setattr(options, 'title', self.video_title)
        setattr(options, 'description', self.video_info)
        setattr(options, 'tags', ",".join(self.video_tags))
        setattr(options, 'client_secrets', self.current_path + "config/client_secret.json")
        setattr(options, 'credentials_file', self.current_path + "config/credentials_file.json")
        setattr(options, 'thumb', self.pic_path)
        setattr(options, 'category', self.info["YOUTUBE_CATEGORY"])
        setattr(options, 'title', self.video_title)

        # options.title = self.video_title
        # options.description = self.video_info
        # options.tags = ",".join(self.video_tags)
        # options.client_secrets = self.current_path + "config/client_secret.json"
        # options.credentials_file = self.current_path + "config/credentials_file.json"
        # options.thumb = self.pic_path
        # options.category = self.info["YOUTUBE_CATEGORY"]

        youtube = main.get_youtube_handler(options)

        if youtube:

            video_id = main.upload_youtube_video(youtube, options, self.video_path, 0, 0)
            video_url = WATCH_VIDEO_URL.format(id=video_id)
            debug("Video URL: {0}".format(video_url))

            if options.thumb:
                youtube.thumbnails().set(videoId=video_id, media_body=options.thumb).execute()

            print(video_url + "\n")
        else:
            raise AuthenticationError("Cannot get youtube resource")

        return video_id

    def bilibili_upload(self):

        uploader = BilibiliUploader()

        # 登录
        uploader.login(self.info["BILIBILI_ACCOUNT"], self.info["BILIBILI_SECRET"])

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
        )

        return avid + "-" + bvid
