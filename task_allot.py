import json
import os
import datetime


from db import ConnectDb

db = ConnectDb()


# 参数初始化函数
def load():
    with open('config.json', encoding='utf-8') as f:
        data = json.load(f)
    return data


conf = load()
# 查询结果包条件
task_type = conf['query_criteria']['task_type']
date = conf['query_criteria']['date']
state = conf['query_criteria']['check_state']
d_t = date.split('-')
start_time = datetime.datetime(int(d_t[0]), int(d_t[1]), int(d_t[2]), 0, 0, 0, 0)
end_time = datetime.datetime(int(d_t[0]), int(d_t[1]), int(d_t[2]), 23, 59, 59, 0)


# 查询任务类别id
def query_category():
    data = db.connect_category().find({"category_name": task_type})
    try:
        category_id = data[0]['_id']
        return category_id
    except IndexError as e:
        print(e, '任务类别查询不到')


# 查询任务包
# 需指定task_type_id
def query_packet(task_type_id):
    data_list = []
    if task_type_id:
        data_all = db.connect_packet().find({"task_type": task_type_id,
                                              "create_time": {"$gte": start_time, "$lte": end_time}, "state": state})
        for data in data_all:
            data_list.append([data["_id"], data["v_num"][-1]])  # 将查到的任务id跟版本号放入列表

    return data_list


# 查询任务json数据
# 需指定packet_id_list
def query_task(packet_list):
    if packet_list:
        for packet_id, v_num in packet_list:
            data_list = db.connect_task().find({'packet_id': packet_id, 'v_num': v_num})  # 根据id跟版本号查询json
            for data in data_list:
                task_id = data['_id']

                img_source = db.connect_img().find({'task_id': task_id})  # 查询img表
                try:
                    img = img_source[0]['img_source']  # 获取图片
                except IndexError as e:
                    print(e)
                    continue

                output_dir = os.path.join(os.getcwd(), 'img', data['json_data']['folder'])
                print(output_dir)
                if not os.path.exists(output_dir):  # 判断用户任务目录是否存在
                    os.makedirs(output_dir)
                img_path = os.path.join(output_dir, data['json_data']['filename'])
                out = open(img_path, 'wb')
                out.write(img)
                out.close()
                with open(str(img_path).replace(".jpg", ".json"), "w") as f:
                    print(str(img_path).replace(".jpg", ".json"))
                    img_json = data
                    json.dump(img_json, f, ensure_ascii=False)

task_type_id = query_category()
packet_list = query_packet(task_type_id)
query_task(packet_list)
