import json, os
from yt_dlp import YoutubeDL

ydl_opts = {
    'writesubtitles': True,
    'subtitlesformat': 'vtt',
    'ignoreerrors': True,
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
    'recode_video': 'mp4',
    'merge_output_format': 'mp4',
    'nocheckcertificate': True,
    'outtmpl': './files/%(title)s-%(id)s.mp4',
    'writethumbnail': True,
    'writeinfojson': True,
}

tt_opts = {
    'writesubtitles': True,
    'subtitlesformat': 'vtt',
    'ignoreerrors': True,
    'recode_video': 'mp4',
    'nocheckcertificate': True,
    'outtmpl': './files/%(id)s.mp4',
    'writethumbnail': True,
    'writeinfojson': True,
}

bili_opts = {
    'ignoreerrors': True,
    'recode_video': 'mp4',
    'merge_output_format': 'mp4',
    'nocheckcertificate': True,
    'outtmpl': './files/%(title)s-%(id)s.mp4',
    'writeinfojson': True,
}

# video_url = "https://www.bilibili.com/video/BV1YF41187Hr"
# video_url = "https://www.tiktok.com/@letsweight/video/7074640188122746158?is_from_webapp=v1&item_id=7074640188122746158"
video_url = "https://www.youtube.com/watch?v=Qb_YE-9njME"
# channel_url = "https://www.youtube.com/channel/UCf3z3UGPivTyGDeLWNREIJw"
channel_url = "https://www.youtube.com/c/%E5%90%8C%E5%92%8C%E5%90%9BHocassian/videos"
choice = "1"


class EasyDownload(object):

    def dl_one(self):

        if choice == "1":
            opt = ydl_opts
        elif choice == "2":
            opt = tt_opts
        else:
            opt = bili_opts

        ydlk = YoutubeDL(opt)
        ydlk.add_default_info_extractors()
        ydlk.extract_info(video_url, download=True)

    def dl_by_channel(self):
        ydl = YoutubeDL(ydl_opts)
        ydl.add_default_info_extractors()
        info = ydl.extract_info(channel_url, download=False)

        # 测试使用
        # with open("full_info.json", 'w') as fp:
        #     json.dump(info, fp)
        # with open("full_info.json", 'r') as f0:
        #     info = json.load(f0)


if __name__ == '__main__':
    vd = EasyDownload()
    vd.dl_one()
