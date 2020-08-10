from pydub import AudioSegment

filename=r'D:\7.21\113\CZW.wav'
save_path=r'D:\7.21\czw.txt'
time = 500*16#600*16 # 1s
rate = 16000

# 切割一段音频

def trans(time):
    time = time // 16
    minute = time//60000
    second = time%60000//1000
    ms = time%1000
    new_time = str(minute)+':'+str(second).zfill(2)+'.'+str(ms).zfill(3)
    return new_time

def load_file():
    wavfile = AudioSegment.from_wav(filename)
    data = wavfile.get_array_of_samples()
    return data

if __name__ == '__main__':
    txt = open(save_path, 'a')
    data = load_file()
    in_audio = 0
    time_cnt = 0
    index_begin = index_end = 0
    index_cnt = 0
    index = []
    for x in data:
        if in_audio: #在单词部分
            if x < 500:
                time_cnt += 1 #间隔超过一秒，判定该单词结束
            if x > 600:
                time_cnt = 0
            if time_cnt > time:
                in_audio = 0 #单词结束
                index_end = index_cnt - time
                index.append(index_begin)
                index.append(index_end)
                print(index_begin)
                print(index_end)
                # print(trans(index_begin))
                # print(trans(index_end))
                # txt.write(index)
                # txt.write('\n')
                print('+++++++++++++++++++++++++++++++')
        else:
            if x > 700: #当振幅超过600时，判定单词开
                if in_audio == 0:
                    index_begin = index_cnt
                in_audio = 1
                time_cnt = 0

        index_cnt += 1
    index_len = len(index)
    txt.write(trans(index[0]))
    txt.write('\n')
    for i in range(2, index_len, 2):
        #print("point is %d"%index[i])
        new_index = (index[i]+index[i-1])//2
        txt.write(trans(new_index))
        txt.write('\n')
    txt.write(trans(index[index_len-1]))
    txt.write('\n')
    txt.close()
