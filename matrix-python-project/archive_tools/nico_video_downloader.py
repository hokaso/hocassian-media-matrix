import nndownload, json

with open("nico_config.json", 'r') as f0:
    nico_config = json.load(f0)

url = "https://www.nicovideo.jp/user/10821010/video"
output_path = "/root/keeno/{title}-{id}.{ext}"
nndownload.execute("-u", nico_config["account"], "-p", nico_config["password"], "-o", output_path, url)
