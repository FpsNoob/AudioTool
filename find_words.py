import os
import re
import shutil
from tensorflow.python.platform import gfile

def load_csv(filepath):
    filename = []
    detail = []
    file = open(filepath, 'r', encoding="utf-8")  # 读取以utf-8
    context = file.read()  # 读取成str
    list_result = context.split("\n")  # 以回车符\n分割成单独的行
    # 每一行的各个元素是以【,】分割的，因此可以
    length = len(list_result)-1
    print(length)
    for i in range(length):
        #print(list_result[i])
        _, x, y = list_result[i].split(", ")
        filename.append(x)
        detail.append(y)
    file.close()
    return filename, detail



def get_words(filepath):
    word_list = []
    file = open(filepath)
    for word in file:
        word = word.rstrip()
        word_list.append(word)
    file.close()
    return word_list

def find_word(folder_path, wanted_word_list):
    '''
    find the sentence in the audio dataset, which including words we wanted
    Args:
        folder_path: folder contains the audio's label
        word_list: the list of words you wanted
    Return:
        the audio's path, filename and details
    '''
    path = []
    file_name = []
    detail = []
    flag = 0
    cnt = 0
    search_path = os.path.join(folder_path, '*', '*.csv')
    for txt_path in gfile.Glob(search_path):
        #txt_file = open(txt_path)
        x, y = load_csv(txt_path)
        file_len = len(x)
        #for txt in txt_file:
        for i in range(file_len):
            # filename, sentence = re.split('\t', txt, 1)
            # sentence = sentence.replace('\n', '').replace('\r', '')
            filename = x[i]
            sentence = y[i]
            words = re.split(' ', sentence)
            #filename = os.path.basename(txt_path).replace('.wav.trn', '')
            for word in words:
                if flag:
                    flag = 0
                    break
                for wanted_word in wanted_word_list:
                    if word.lower() == wanted_word.lower():
                        path.append(txt_path)
                        file_name.append(filename)
                        detail.append(sentence)
                        print('---------------------------------------')
                        print(filename)
                        print(word)
                        print('Find words in the %s' % txt_path)
                        print(sentence)
                        flag = 1
                        break
        #txt_file.close()
    return path, file_name, detail

def copy_file(path, file_name, detail, save_path):
    file = open(save_path + '\index.txt', 'a')
    print(save_path)
    path_len = len(path)
    # copy file
    cnt = 0
    for i in range(path_len):
        temp_name = file_name[i] + '.wav'
        loadpath = os.path.dirname(path[i])
        loadpath = os.path.join(loadpath, temp_name)
        savepath = os.path.join(save_path, temp_name)
        shutil.copyfile(loadpath, savepath)
        cnt += 1
        print('copy %s to %s' % (loadpath, savepath))
        file.write(file_name[i]+'.wav' + '\t')
        file.write(detail[i])
        file.write('\n')
    print('total copy file %d' % cnt)
    file.close()

def word_count(filepath, wanted_word_list_):
    word_list = {}
    for wanted_word in wanted_word_list_:
        word_list[wanted_word.lower()] = 0
    print(word_list)
    search_path = os.path.join(filepath, '*', '*.csv')
    for path in gfile.Glob(search_path):
        # txt_file = open(txt_path)
        x, y = load_csv(path)
        file_len = len(x)
        # for txt in txt_file:
        for i in range(file_len):
            # filename, sentence = re.split('\t', txt, 1)
            # sentence = sentence.replace('\n', '').replace('\r', '')
            filename = x[i]
            sentence = y[i]
            words = re.split(' ', sentence)
            for word in words:
                for wanted_word in wanted_word_list_:
                    if word.lower() == wanted_word.lower():
                        print('---------------------------------------')
                        print(filename)
                        print(word)
                        print(sentence)
                        word_list[word.lower()] += 1
    for word in wanted_word_list_:
        print('%s: %d' % (word, word_list[word.lower()]))



if __name__ == '__main__':
    load_path = r'D:\chrome\Crowdsourced high-quality UK and Ireland English Dialect speech data set'
    save_path = r'D:\words_count\temp_16'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    word_list = get_words(r'words.txt')
    for word in word_list:
        print(word)
    path, file_name, detail = find_word(load_path, word_list)
    copy_file(path, file_name, detail, save_path)
    word_count(load_path, word_list)
