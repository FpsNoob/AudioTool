#基于短时能量的方法获取音频中的语音段
from pydub import AudioSegment
import math
import matplotlib.pyplot as plt

def get_sample(file_path):
    #加载wav文件, 获取该音频的采样率
    wavfile = AudioSegment.from_wav(file_path)
    #转化成numpy数组形式
    wavfile = wavfile.get_array_of_samples()
    return wavfile

def get_energy(wavfile, frame_length):
    # 计算帧数
    frame_number = round(len(wavfile)/frame_length)
    print(frame_number)
    # 分帧处理数据
    E = []
    for i in range(1, frame_number+1):
        signals = wavfile[(i-1)*frame_length:i*frame_length-1]
        energy = 0
        for signal in signals:
            energy += energy + math.pow(signal, 2)
        E.append(energy)
    return E

if __name__ == '__main__':
    file_path=r'D:\Audio_0720_0722\7.20\113\113_LZH\lzh_Albert_1.wav'
    frame_length = 200
    wavfile = get_sample(file_path)

    E = get_energy(wavfile, frame_length)
    figure = plt.figure(1)
    fig1 = figure.add_subplot(2,1,1)
    fig2 = figure.add_subplot(2,1,2)
    fig1.plot(wavfile)
    fig2.plot(E)
    plt.show()


