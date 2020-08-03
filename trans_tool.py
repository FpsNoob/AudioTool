import os
from tensorflow.python.platform import gfile


def trans_audiofile(file_path, file_format, new_format):
    # 在文件夹下查找该格式的文件
    cnt = 0
    search_path = os.path.join(file_path, '*', '*'+file_format)
    for path in gfile.Glob(search_path):
        cnt += 1
        save_path = path.replace(file_format, new_format)
        cmd = 'ffmpeg -i ' + path + ' ' + save_path
        print(cmd)
        os.system(cmd)
    print('totally trans %d files' % cnt)

def file_remove(path, file_format):
    search_path = os.path.join(file_path, '*', '*' + file_format)
    cnt = 0
    for path in gfile.Glob(search_path):
        os.remove(path)
        print(path)
        cnt += 1
    print('delete %d files' % cnt)


if __name__ == '__main__':
    file_path = r'D:\chrome\words_temp'
    file_format = '.sph'
    new_format = '.wav'
    trans_audiofile(file_path, file_format, new_format)
    file_remove(file_path, file_format)