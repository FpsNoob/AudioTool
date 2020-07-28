import re
import os
import find_error
from pydub import AudioSegment

path = r'D:\7.21'
wav_path = path + '\\116\\CZW.wav'
time_path = path + '\\czw.txt'
word_path = path + '\\words.txt'
name = 'czw_'
save_path = r"D:\7.21\116\CZW"
value = find_error.get_value() #设备之间的偏差
word_index = 0
cnt = 1

def get_wav_make(wavfile, begin, end, filename):
    cut_wav = wavfile[begin:end]
    cut_wav.export(save_path+'\\'+name+filename+'.wav', format='wav')    # save new wavfile
    print("clip %s: %d to %d" % (filename, begin, end))

def trans(minute, second, ms, value):
    result = int(ms) + int(second) * 1000 + int(minute) * 60000
    result += value
    return result

def get_timestamp(wav_path, time_path, words, word_index, cnt):
    time_stamp = open(time_path)
    wavfile = AudioSegment.from_wav(wav_path)
    duration = wavfile.duration_seconds * 1000  # 音频时长（ms）
    begin = end = 0
    flag = 0
    error = 0
    for line in time_stamp.readlines():
        if line in ['\n']:
            word_index += 1
            cnt = 1
            continue
        if line == 'error\n':
            error = 1
            continue
        line = line.rstrip()
        [minute, second, ms] = re.split('[:.]', line)
        if flag == 0:
            begin = end = trans(minute, second, ms, value)
            flag = 1
        elif error == 1: #噪声错误
            begin = end = trans(minute, second, ms, value)
            error = 0
            continue
        else:
            begin = end
            end = trans(minute, second, ms, value)
        if end > duration:
            end = duration
        if begin < end:
            if word_index > 33:
                print('The audio of %s is over.' % name)
                exit(0)
            #print("clip %s: %d to %d" % (words[word_index] + '_' + str(cnt), begin, end))

            get_wav_make(wavfile, begin, end,
                         words[word_index] + '_' + str(cnt))
            cnt += 1
    print('the length of aduio is %d' % duration)
    time_stamp.close()

def get_list(path):
    words = open(path)
    list = []
    for line in words:
        line = line.replace(' ', '_')
        list.append(line.rstrip())
    words.close()
    return list


if __name__ == '__main__':
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    words = get_list(word_path)
    get_timestamp(wav_path, time_path, words, word_index, cnt)
   # print(trans(10, 0, 796, value))
    # print(trans(5, 23, 430))








