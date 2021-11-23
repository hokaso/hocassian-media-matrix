import sys, os, json, copy, random, time
sys.path.append(os.getcwd())
from db.db_pool_handler import InstantDBPool
from youtube_upload import main

WATCH_VIDEO_URL = "https://www.youtube.com/watch?v={id}"

class AuthenticationError(Exception): pass

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

        # 完成YouTube上传
        self.youtube_upload()

        return video_title, video_info



    def youtube_upload(self):

        options = None
        options.title = self.video_title
        options.description = self.video_info
        options.tags = ",".join(self.video_tags)
        options.client_secrets = self.current_path + ""
        options.credentials_file = ""
        options.thumb = ""
        options.category = "Travel & Events"

        video_path = ""

        youtube = main.get_youtube_handler(options)

        if youtube:

            video_id = main.upload_youtube_video(youtube, options, video_path, 0, 0)
            video_url = WATCH_VIDEO_URL.format(id=video_id)
            debug("Video URL: {0}".format(video_url))

            if options.thumb:
                youtube.thumbnails().set(videoId=video_id, media_body=options.thumb).execute()
            if options.playlist:
                playlists.add_video_to_playlist(youtube, video_id,
                                                title=lib.to_utf8(options.playlist), privacy=options.privacy)
            print(video_url + "\n")
        else:
            raise AuthenticationError("Cannot get youtube resource")