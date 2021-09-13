import pymysql
from dbutils.pooled_db import PooledDB


class DBPoolHandler(object):

    def __init__(self, host, port, user, password, database):
        self.POOL = PooledDB(

            # 使用连接数据库的模块
            creator=pymysql,

            # 连接池允许的最大连接数，0和None表示不限制连接数
            maxconnections=6,

            # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            mincached=2,

            # 链接池中最多闲置的链接，0和None不限制
            maxcached=5,

            # 链接池中最多共享的链接数量，0和None表示全部共享（无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享）
            maxshared=3,

            # 连接池中如果没有可用连接后，是否阻塞等待（True - 等待；False - 不等待然后报错）
            blocking=True,

            # 一个链接最多被重复使用的次数，None表示无限制
            maxusage=None,

            # 开始会话前执行的命令列表。如：["set datestyle to ……", "set time zone ……"]
            setsession=[],

            # 「ping」MySQL服务端，检查是否服务可用（详见组件注释）
            ping=0,

            # 以下为基本参数
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8'
        )

    def __new__(cls, *args, **kw):
        """
        启用单例模式
        :param args:
        :param kw:
        :return:
        """
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def connect(self):
        """
        启动连接
        :return:
        """
        conn = self.POOL.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.ping(conn)
        return conn, cursor

    @staticmethod
    def ping(conn):
        conn.ping(reconnect=True)

    @staticmethod
    def connect_close(conn, cursor):
        """
        关闭连接
        :param conn:
        :param cursor:
        :return:
        """
        cursor.close()
        conn.close()

    def search(self, sql, *args):
        """
        批量查询
        :param sql:
        :param args:
        :return:
        """

        conn, cursor = self.connect()
        cursor.execute(sql, *args)
        # record = cursor.fetchone()
        record_list = cursor.fetchall()
        self.connect_close(conn, cursor)
        return record_list

    def modify(self, sql, *args):
        """
        插入数据
        :param sql:
        :param args:
        :return:
        """
        conn, cursor = self.connect()
        row = cursor.execute(sql, *args)
        conn.commit()
        self.connect_close(conn, cursor)
        return row


class InstantDB(object):

    def __init__(self):
        with open(os.getcwd() + "/db/config.json", 'r') as f0:
            info = json.load(f0)

            # 本地生產
            # self.db_handle = DBPoolHandler(
            #     info["local_prod"]["ip"],
            #     info["local_prod"]["account"],
            #     info["local_prod"]["password"],
            #     info["local_prod"]["database"],
            #     info["local_prod"]["port"]
            # )

            # 遠程生產
            # self.db_handle = DBPoolHandler(
            #     info["remote_prod"]["ip"],
            #     info["remote_prod"]["account"],
            #     info["remote_prod"]["password"],
            #     info["remote_prod"]["database"],
            #     info["remote_prod"]["port"]
            # )

            # 本地開發
            self.db_handle = DBPoolHandler(
                host=info["local_dev"]["ip"],
                user=info["local_dev"]["account"],
                password=info["local_dev"]["password"],
                database=info["local_dev"]["database"],
                port=info["local_dev"]["port"]
            )

    def get_connect(self):
        return self.db_handle
