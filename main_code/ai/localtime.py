import time
# 生成当地的精确时间


def localtime():
    return time.asctime(time.localtime(time.time()))
