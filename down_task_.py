import os

import paramiko
import json
from stat import S_ISDIR as isdir


def load():
    with open('config.json', encoding='utf-8') as f:
        data = json.load(f)
    return data


# 获取数据库配置
mongodb_config = load()['dbconf']
# 获取云盘配置
cloud_config = load()['cloud_config']


def down_from_remote(sftp_obj, remote_dir_name, local_dir_name):
    """远程下载文件"""
    remote_file = sftp_obj.stat(remote_dir_name)
    if isdir(remote_file.st_mode):
        # 文件夹，不能直接下载，需要继续循环
        check_local_dir(local_dir_name)
        print('开始下载文件夹：' + remote_dir_name)
        for remote_file_name in sftp.listdir(remote_dir_name):
            sub_remote = os.path.join(remote_dir_name, remote_file_name)
            sub_remote = sub_remote.replace('\\', '/')
            sub_local = os.path.join(local_dir_name, remote_file_name)
            sub_local = sub_local.replace('\\', '/')
            down_from_remote(sftp_obj, sub_remote, sub_local)
    else:
        # 文件，直接下载
        print('开始下载文件：' + remote_dir_name)
        sftp.get(remote_dir_name, local_dir_name)


def check_local_dir(local_dir_name):
    if not os.path.exists(local_dir_name):  # 判断用户任务目录是否存在
        os.makedirs(local_dir_name)


if __name__ == "__main__":
    """程序主入口"""
    # 服务器连接信息
    host_name = cloud_config['host']
    user_name = cloud_config['username']
    password = cloud_config['password']
    port = cloud_config['port']
    # 远程文件路径（需要绝对路径）
    remote_dir = cloud_config['put_path']
    # 本地文件存放路径（绝对路径或者相对路径都可以）
    local_dir = cloud_config['local_path']

    # 连接远程服务器
    t = paramiko.Transport((host_name, port))
    t.connect(username=user_name, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)

    # 远程文件开始上传
    down_from_remote(sftp, remote_dir, local_dir)

    # 关闭连接
    t.close()
