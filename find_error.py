import re

def trans(line):
    [minute, second, ms] = re.split('[:.]', line)
    result = int(ms) + int(second) * 1000 + int(minute) * 60000
    return result

def get_value():  #对齐不同设备，同一段音频的起始
    error = trans('  0:03.344') - trans('  0:03.474')
    print(error)
    return error
