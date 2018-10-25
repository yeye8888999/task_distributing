import os
import zipfile
import paramiko
import json


def load():
    with open('config.json', encoding='utf-8') as f:
        data = json.load(f)
    return data


# 获取数据库配置
mongodb_config = load()['dbconf']
# 获取云盘配置
cloud_config = load()['cloud_config']


def put_from_local(remote_dir_name, local_dir_name):
    """远程上传文件"""
    list = []
    for root, dirs, files in os.walk(local_dir_name):
        for dir in dirs:
            out_path = os.path.join(local_dir_name+"\\"+dir+".zip")  # 压缩任务包路径
            dir_path = os.path.join(local_dir_name+"\\"+dir)   # 任务包文件路径
            make_zip(local_dir_name, out_path, dir_path)

    for fl_file in os.listdir(local_dir_name):
        if fl_file.endswith('zip'):
            list.append(fl_file)

        else:
            continue
    for i in list:
        sub_remote = os.path.join(remote_dir_name, i)
        sub_remote = sub_remote.replace('\\', '/')
        sub_local = os.path.join(local_dir_name, i)
        sub_local = sub_local.replace('\\', '/')
        print('开始上传文件：' + i)
        sftp.put(sub_local, sub_remote)
        print('上传文件成功：' + i)


# 打包文件夹
def make_zip(source_dir, output_filename, dir_path):
    a = 777
    os.chmod(source_dir, a)
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(dir_path))
    for parent, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)     #相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


def ssh_command(host_name, port, user_name, password):
    """启动服务"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_name, port, user_name, password)
        # 使用ssh命令对网盘进行刷新
        ssh.exec_command('docker exec -t netdisk_dev sudo -u www-data php occ files:scan --all')
        print("check status %s OK\n" % host_name)
        ssh.close()
    except Exception as ex:
        print("\tError %s\n" % ex)


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
    put_from_local(remote_dir, local_dir)
    # 关闭连接
    t.close()
    ssh_command(host_name, port, user_name, password)

