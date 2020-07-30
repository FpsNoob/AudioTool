import os
import re
from tensorflow.python.platform import gfile

def get_words(filepath):
    word_list = []
    file = open(filepath)
    for word in file:
        word_list.append(word)
    file.close()
    return word_list

def find_word(folder_path, word_list):
    need_to_save = []
    search_path = os.path.join(folder_path, '*', '*.txt')
    for txt_path in gfile.Glob(search_path):
        txt_file = open(txt_path)
        for sentence in txt_file:
            for word in word_list:
                if re.search(word, sentence, re.IGNORECASE):
                    need_to_save.append(sentence)
                    print(sentence)
        txt_file.close()
    return need_to_save


if __name__ == '__main__':
    word_list = get_words(r'D:\Audio_0720_0722\7.20\words.txt')
    need_to_save = find_word(r'D:\chrome\Free ST American English Corpus', word_list)
    f = open(r'D:\chrome\word_in_sentence.txt', 'a')
    for sentence in need_to_save:
        f.write(sentence)
        f.write('\n')
    f.close()
