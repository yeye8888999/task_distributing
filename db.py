import json
from pymongo import MongoClient


# 参数初始化函数
def load():
    with open('config.json', encoding='utf-8') as f:
        data = json.load(f)
    return data


conf = load()

# 数据库连接
db_host_ip = conf['dbconf']['host']
db_port = conf['dbconf']['port']
db_name = conf['dbconf']['database']
db_category_collection = conf['dbconf']['category_collection']  # 任务类别
db_packet_collection = conf['dbconf']['packet_collection']  # 任务包
db_task_collection = conf['dbconf']['task_collection']  # 任务json数据
db_img_collection = conf['dbconf']['img_collection']  # 任务图片


class ConnectDb():
    def __init__(self):
        self.client = MongoClient(db_host_ip, db_port)
        # 获得一个database
        self.db = self.client[db_name]

    # 任务类别
    def connect_category(self):
        col_category = self.db[db_category_collection]
        return col_category

    # 任务包
    def connect_packet(self):
        col_packet = self.db[db_packet_collection]
        return col_packet

    # 任务json数据
    def connect_task(self):
        col_task = self.db[db_task_collection]
        return col_task

    # 任务图片
    def connect_img(self):
        col_img = self.db[db_img_collection]
        return col_img

