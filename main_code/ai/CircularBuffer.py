# Mrl-环形缓存
# 可能用不到了
import copy
import os
import pickle
from collections import deque

from main_code.const import *
from localtime import *


# [st-1, at-1, rt, st, ct]
class Red:
    def __init__(self, maxsize, save_rate=300):
        self.maxsize = maxsize
        self.save_count = 0
        self.rlmemory = deque(maxlen=self.maxsize)
        self.save_rate = save_rate
        try:
            with open("Mrl_red.buf", "rb") as Mrl_red:
                while self.rlmemory.__len__() < self.maxsize:
                    try:
                        self.rlmemory.append(pickle.load(Mrl_red))
                    except:
                        break
        except:
            pass

    def save(self):
        try:
            os.rename("Mrl_red.buf", f'Mrl_red_{localtime()}.buf')
        except:
            pass
        with open("Mrl_red.buf", "wb") as Mrl_red:
            memory = copy.deepcopy(self.rlmemory)
            while memory.__len__() > 0:
                tup = tuple(memory.popleft())
                pickle.dump(tup, Mrl_red)

    def update(self, tup):
        if self.rlmemory.__len__() < self.maxsize:
            self.rlmemory.append(tup)
        elif self.rlmemory.__len__() == self.maxsize:
            self.rlmemory.popleft()
            self.rlmemory.append(tup)
        self.save_count += 1
        if self.save_count > self.save_rate:
            self.save()
            self.save_count = 0


class Black:
    def __init__(self, maxsize, save_rate=300):
        self.maxsize = maxsize
        self.save_count = 0
        self.rlmemory = deque(maxlen=self.maxsize)
        self.save_rate = save_rate
        try:
            with open("Mrl_black.buf", "rb") as Mrl_black:
                while self.rlmemory.__len__() < self.maxsize:
                    try:
                        self.rlmemory.append(pickle.load(Mrl_black))
                    except:
                        break
        except:
            pass

    def save(self):
        try:
            os.rename("Mrl_black.buf", f'Mrl_black_{localtime()}.buf')
        except:
            pass
        with open("Mrl_black.buf", "wb") as Mrl_black:
            memory = copy.deepcopy(self.rlmemory)
            while memory.__len__() > 0:
                tup = tuple(memory.popleft())
                pickle.dump(tup, Mrl_black)

    def update(self, tup):
        if self.rlmemory.__len__() < self.maxsize:
            self.rlmemory.append(tup)
        elif self.rlmemory.__len__() == self.maxsize:
            self.rlmemory.popleft()
            self.rlmemory.append(tup)
        self.save_count += 1
        if self.save_count > self.save_rate:
            self.save()
            self.save_count = 0


class CircularBuffer:
    def __init__(self, maxsize=1000):
        self.maxsize = maxsize
        self.red = Red(self.maxsize)
        self.black = Black(self.maxsize)

    def update(self, tup, camp):
        if camp == camp_red:
            self.red.update(tup)
        else:
            self.black.update(tup)

    def save(self):
        self.red.save()
        self.black.save()
