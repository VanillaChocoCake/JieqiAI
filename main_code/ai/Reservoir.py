# Msl-蓄水池 (st,at)
import os
import pickle
from localtime import *
import random
import numpy as np
from const import *


class Red:
    def __init__(self, maxsize, save_rate=200):
        self.slmemory = []
        self.maxsize = maxsize
        self.st = []
        self.at = []
        self.save_count = 0
        self.save_rate = save_rate
        try:
            with open("Msl_red.buf", "rb") as Msl_red:
                while True:
                    try:
                        if len(self.slmemory) < self.maxsize:
                            self.slmemory.append(pickle.load(Msl_red))
                        else:
                            num = random.randint(0, self.maxsize - 1)
                            self.slmemory[num] = pickle.load(Msl_red)
                    except:
                        break
        except:
            pass
        for i in range(0, len(self.slmemory)):
            self.st.append(self.slmemory[i][0])
            self.at.append(self.slmemory[i][1])
        self.st = np.array(self.st)
        self.at = np.array(self.at)

    def save(self):
        try:
            os.rename("Msl_red.buf", f'Msl_red_{localtime()}.buf')
        except:
            pass
        with open("Msl_red.buf", "wb") as Msl:
            for i in range(0, len(self.slmemory)):
                tup = tuple(self.slmemory[i])
                pickle.dump(tup, Msl)

    def update(self, tup):
        if len(self.slmemory) < self.maxsize:
            self.slmemory = list(self.slmemory)
            self.slmemory.append(tup)
            self.slmemory = np.array(self.slmemory)
            self.st = list(self.st)
            self.st.append(tup[0])
            self.st = np.array(self.st)
            self.at = list(self.at)
            self.at.append(tup[1])
            self.at = np.array(self.at)
        else:
            num = random.randint(0, self.maxsize - 1)
            self.slmemory[num] = tup
            self.st[num] = tup[0]
            self.at[num] = tup[1]
        self.save_count += 1
        if self.save_count > self.save_rate:
            self.save()
            self.save_count = 0


class Black:
    def __init__(self, maxsize, save_rate=200):
        self.slmemory = []
        self.maxsize = maxsize
        self.st = []
        self.at = []
        self.save_count = 0
        self.save_rate = save_rate
        try:
            with open("Msl_black.buf", "rb") as Msl_black:
                while True:
                    try:
                        if len(self.slmemory) < self.maxsize:
                            self.slmemory.append(pickle.load(Msl_black))
                        else:
                            num = random.randint(0, self.maxsize - 1)
                            self.slmemory[num] = pickle.load(Msl_black)
                    except:
                        break
        except:
            pass
        for i in range(0, len(self.slmemory)):
            self.st.append(self.slmemory[i][0])
            self.at.append(self.slmemory[i][1])
        self.st = np.array(self.st)
        self.at = np.array(self.at)

    def save(self):
        try:
            os.rename("Msl_black.buf", f'Msl_black_{localtime()}.buf')
        except:
            pass
        with open("Msl_black.buf", "wb") as Msl:
            for i in range(0, len(self.slmemory)):
                tup = tuple(self.slmemory[i])
                pickle.dump(tup, Msl)

    def update(self, tup):
        if len(self.slmemory) < self.maxsize:
            self.slmemory = list(self.slmemory)
            self.slmemory.append(tup)
            self.slmemory = np.array(self.slmemory)
            self.st = list(self.st)
            self.st.append(tup[0])
            self.st = np.array(self.st)
            self.at = list(self.at)
            self.at.append(tup[1])
            self.at = np.array(self.at)
        else:
            num = random.randint(0, self.maxsize - 1)
            self.slmemory[num] = tup
            self.st[num] = tup[0]
            self.at[num] = tup[1]
        self.save_count += 1
        if self.save_count > self.save_rate:
            self.save()
            self.save_count = 0


class Reservoir:
    def __init__(self, maxsize=3000):
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
