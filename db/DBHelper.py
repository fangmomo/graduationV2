import pymysql
import logging
import sys
import json

# 加入日志
# 获取logger实例
from app.db.db_config import db_config

logger = logging.getLogger()
# 指定输出格式
formatter = logging.Formatter('%(asctime)s\
              %(levelname)-8s:%(message)s')
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 为logger添加具体的日志处理器
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)


class DBHelper:
    # 构造函数,初始化数据库连接
    def __init__(self):
        self.host = db_config['host']
        self.user = db_config['username']
        self.password = db_config['password']
        self.port = db_config['port']
        self.dbname = db_config['database']
        self.conn = None  # 连接
        self.cur = None  # 游标

    def connectDB(self):
        # noinspection PyBroadException
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port,
                                        db=self.dbname, charset=db_config['charset'])  # 创建连接
            self.cur = self.conn.cursor(pymysql.cursors.DictCursor)  # 创建游标
        except BaseException as e:
            logger.error(e)
            logger.error("connectDatabase failed")
            return False
        return True

    # 关闭数据库
    def closeDB(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql):
        self.connectDB()
        # noinspection PyBroadException
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.execute(sql)
                self.conn.commit()
        except BaseException as f:
            logger.error("error: " + json.dump(f))
            logger.error("execute failed: " + sql)
            logger.error("params: " + self.params)
            self.conn.rollback()
            self.closeDB()
            return False
        return self.cur.rowcount

    # 用来查询表数据
    def select(self, sql):
        self.connectDB()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def executemany(self, sql, params):
        print(sql)
        print(params)
        self.connectDB()
        """
        批量插入数据
        :param sql:    插入数据模版, 需要指定列和可替换字符串个数
        :param params:  插入所需数据，列表嵌套元组[(1, '张三', '男'),(2, '李四', '女'),]
        :return:    影响行数
        """
        try:
            # sql = "INSERT INTO USER VALUES (%s,%s,%s,%s)"  # insert 模版
            # params = [(2, 'fighter01', 'admin', 'sanpang'),
            #           (3, 'fighter02', 'admin', 'sanpang')]  # insert数据，
            self.cur.executemany(sql, params)
            self.conn.commit()

        except BaseException as f:
            print(f)
            logger.error("execute failed: " + sql)
            logger.error("params: " + json.dumps(params))
            self.conn.rollback()
            self.closeDB()
        return self.cur.rowcount

    def __enter__(self):

        self.connectDB()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时关闭游标关闭连接"""
        self.cur.close()
        self.conn.close()
