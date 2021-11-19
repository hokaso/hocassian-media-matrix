import sys, os, json, copy
sys.path.append(os.getcwd())
from db.db_pool_handler import InstantDBPool

class Upload(object):

    def __init__(self, FLOW_ID):

        with open("auto_distribute/config.json", 'r') as f0:
            info = json.load(f0)

