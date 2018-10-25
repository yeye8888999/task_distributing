import os, zipfile

a = 777
def make_zip(source_dir, output_filename):

    os.chmod(source_dir, a)
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)     #相对路径
            zipf.write(pathfile, arcname)
    zipf.close()




local_path= "C:\\Users\\shihua.wang\\Desktop\\task_distributing\\img\\20180921143333_1"
out_path = "C:\\Users\\shihua.wang\\Desktop\\filename.zip"
make_zip(local_path,out_path)