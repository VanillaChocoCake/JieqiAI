import time
# 生成当地的精确时间


def localtime():
    res = time.asctime(time.localtime(time.time())).split(" ")
    year = res[4]
    month = res[1]
    day = res[2]
    exact_time = res[3].split(":")
    hour = exact_time[0]
    minute = exact_time[1]
    second = exact_time[2]
    res = f'{year}_{month}_{day}_{hour}_{minute}_{second}'
    return res
