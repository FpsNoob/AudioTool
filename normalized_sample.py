#基于短时能量的方法获取音频中的语音段
from pydub import AudioSegment
import math
import os
import re
import matplotlib.pyplot as plt
import numpy as np

FRAME = 16 #样本采样率kHz
minlen = 50

def get_wavfile(file_path):
    #加载wav文件, 获取该音频的采样率
    wavfile = AudioSegment.from_file(file_path)
    #转化成numpy数组形式
    return wavfile

def get_energy_zcr(wavfile, frame_length):
    # 计算帧数
    wavfile = wavfile.get_array_of_samples()
    frame_number = round(len(wavfile)/frame_length)
    # 分帧处理数据
    E = []
    Z = []
    for i in range(1, frame_number+1):
        signals = wavfile[(i-1)*frame_length:i*frame_length]
        energy = 0
        cnt = 0
        for signal in signals:
            energy += energy + math.pow(signal, 2)
        for j in range(len(signals)-1):
            if (signals[j]*signals[j+1])<0:
                cnt += 1
        Z.append(cnt)
        E.append(energy)
    return E, Z, np.mean(E)

def get_audiopart(energy, zcr, E_avg, t3):
    is_audio =0
    silence_len = 0
    D = C = len(energy)
    for i in range(len(energy)):
        if energy[i] > E_avg and C > i:#语音开始
            is_audio = 1
            C = i
        if is_audio:   #在语音段中
            if energy[i] < E_avg: #如果出现连续静音段的长度
                silence_len += 1
            if silence_len > minlen: #进入语音段后出现过长静音，语音段结束
                is_audio = 0
                D = i - silence_len
        if (D-C) > minlen: #语音段长度足够
            break
    print(C)
    print(D)
    A = C
    B = D
    mid = (D+C)/2
    for i in range(C, -1, -1):
        if zcr[i] > t3:
            A = i
    for i in range(D, len(zcr)):
        if zcr[i] > t3:
            B = i
    print(A)
    print(B)
    print(mid)
    return A, B, mid


def to_normalized(wavfile, begin, end, mid, frame_length, want_length, save_path, filename, titil):
    begin = begin*frame_length/FRAME
    end = end*frame_length/FRAME
    mid = mid*frame_length/FRAME
    if (mid - begin)>(want_length/2):
        begin = mid - want_length/2
    if (end - mid)>(want_length/2):
        end = mid + want_length/2
    print('audio part is %f to %f' % (begin, end))
    cut_wav = wavfile[begin:end]
    silence_length = (want_length - cut_wav.duration_seconds*1000)/2
    if silence_length>0:
        silence = AudioSegment.silent(duration=silence_length, frame_rate=16000)
        cut_wav = silence + cut_wav + silence
    # str = re.sub('\d+', '', filename)
    # str = re.sub('_.wav', '', str)
    # name, label = re.split('_', str, 1)
    # save_path = save_path+'\\'+label
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_path = os.path.join(save_path, filename)
    cut_wav.export(save_path, format='wav')  # save new wavfile
    print('Dealing .....')
    print(save_path)
    print('-----------------------')


if __name__ == '__main__':
    folder_path = r'D:\speech_commands_v0.02'
    save_path = r'D:\speech_commands_2s'
    frame_length = 100
    want_length = 2000 #ms

    g = os.walk(folder_path)
    for path, d, filelist in g:
        for filename in filelist:
            fulepath = os.path.join(path, filename)
            _, label = os.path.split(path)
            print(fulepath)
            wavfile = get_wavfile(fulepath)
            energy, zcr, energy_avg = get_energy_zcr(wavfile, frame_length)
            begin, end, mid = get_audiopart(energy, zcr, energy_avg, (max(zcr)+min(zcr))/2)
            to_normalized(wavfile, begin, end, mid, frame_length,
                          want_length, save_path, filename, label)



    # wavfile = get_wavfile(r'D:\Test_data\113\CHX\chx_Albert_10.wav')
    # energy, zcr, energy_avg = get_energy_zcr(wavfile, frame_length)
    # begin, end, mid = get_audiopart(energy, zcr, energy_avg, (max(zcr)+min(zcr))/2)
    # to_normalized(wavfile, begin, end, mid, frame_length,
    #               want_length, save_path, 'test.wav')
    #
    # figure = plt.figure(1)
    # fig1 = figure.add_subplot(3,1,1)
    # fig2 = figure.add_subplot(3,1,2)
    # fig3 = figure.add_subplot(3,1,3)
    # fig1.plot(wavfile.get_array_of_samples())
    # fig2.set_ylim(min(energy), max(energy))
    # fig2.plot(energy)
    # fig2.axhline(energy_avg, color='red', linestyle='--')
    # fig3.plot(zcr)
    # fig3.axhline((max(zcr)+min(zcr))/2, color='red', linestyle='--')
    # plt.show()


