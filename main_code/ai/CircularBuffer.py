# Mrl-环形缓存
# 可能用不到了
import pickle
from queue import Queue
import os
from localtime import *
import numpy as np
from const import *


class CircularBuffer:
    def __init__(self):
        self.maxsize = 300
        self.red_rlmemory = Queue(maxsize=self.maxsize)
        self.black_rlmemory = Queue(maxsize=self.maxsize)
        with open("Mrl_red.buf", "rb") as Mrl_red:
            while self.red_rlmemory.qsize() < self.maxsize:
                try:
                    self.red_rlmemory.put(pickle.load(Mrl_red))
                except:
                    break
        with open("Mrl_black.buf", "rb") as Mrl_black:
            while self.black_rlmemory.qsize() < self.maxsize:
                try:
                    self.black_rlmemory.put(pickle.load(Mrl_black))
                except:
                    break

    def update(self, tup, camp):
        if camp == camp_red:
            if self.red_rlmemory.qsize() < self.maxsize:
                self.red_rlmemory.put(tup)
            elif self.red_rlmemory.qsize() == self.maxsize:
                self.red_rlmemory.get()
                self.red_rlmemory.put(tup)
        else:
            if self.black_rlmemory.qsize() < self.maxsize:
                self.black_rlmemory.put(tup)
            elif self.black_rlmemory.qsize() == self.maxsize:
                self.black_rlmemory.get()
                self.black_rlmemory.put(tup)

    def save(self):
        os.rename("Mrl_red.buf", "Mrl_red " + localtime() + ".buf")
        os.rename("Mrl_black.buf", "Mrl_black " + localtime() + ".buf")
        with open("Mrl_red.buf.buf", "wb") as Mrl_red:
            while self.red_rlmemory.qsize() > 0:
                tup = tuple(self.red_rlmemory.get())
                pickle.dump(tup, Mrl_red)
        with open("Mrl_black.buf.buf", "wb") as Mrl_black:
            while self.black_rlmemory.qsize() > 0:
                tup = tuple(self.black_rlmemory.get())
                pickle.dump(tup, Mrl_black)
