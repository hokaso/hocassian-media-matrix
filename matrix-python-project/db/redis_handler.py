import redis

class InstantRedis(object):

    def __init__(self):
        # 初始化数据库
        host = 'localhost'
        port = 6379
        pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
        self.redis_handle = redis.Redis(connection_pool=pool)

    def get_redis_connect(self):
        return self.redis_handle
