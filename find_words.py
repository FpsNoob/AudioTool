import os
import re
from tensorflow.python.platform import gfile

def get_words(filepath):
    word_list = []
    file = open(filepath)
    for word in file.readlines():
        word_list.append(word)
    file.close()
    return word_list

def find_word(folder_path, word_list):
    '''
    find the sentence in the audio dataset, which including words we wanted
    Args:
        folder_path: folder contains the audio's label
        word_list: the list of words you wanted
    Return:
        the path to the audio
        aud
    '''
    need_to_save = []
    search_path = os.path.join(folder_path, '*', '*.txt')
    for txt_path in gfile.Glob(search_path):
        txt_file = open(txt_path)
        for sentence in txt_file:
            print(sentence)
            for word in word_list:
                if re.search(word, sentence, re.IGNORECASE):
                    need_to_save.append(txt_path)
                    need_to_save.append(sentence)
                    need_to_save.append('--------------------------------')
                    print('---------------------------------------')
                    print('Find words in the %s' % txt_path)
                    print(sentence)
        txt_file.close()
    return need_to_save

def copy_file():
    ''' copy the file to the path we set, which is uses the label saved in find_word function
        Agrs:
         file name

    '''

if __name__ == '__main__':
    word_list = get_words(r'words.txt')
    for word in word_list:
        print(word)
    need_to_save = find_word(r'D:\chrome\Free_ST', word_list)
    f = open(r'D:\chrome\path_1.txt', 'a')
    for sentence in need_to_save:
        f.write(sentence)
        f.write('\n')
    f.close()
    # find words
