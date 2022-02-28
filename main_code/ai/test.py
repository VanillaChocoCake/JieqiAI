import copy

import numpy as np
from tensorflow.keras import models
from AI_Functions import *
from main_code.game.Train.GAME_Functions import *
from const import *
import pickle
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D, Dense, MaxPooling2D, MaxPooling3D
from tensorflow.keras.layers import add, BatchNormalization, Flatten
from tensorflow.keras.losses import CategoricalCrossentropy, MeanSquaredError
import tensorflow as tf
import tensorflow.keras as keras
from localtime import localtime
import os
from const import *
from SL import *
from Reservoir import Reservoir

"""
# train
red_model = SLModel()
Msl = Reservoir()
red_model.train(Msl.red.st, Msl.red.at, camp_red, epochs=100)
"""

# test
red_model = SLModel(model=models.load_model("sl_model_red.h5"))
temp = []
with open("st.data", "rb") as data:
    while True:
        try:
            temp.append(pickle.load(data))
        except:
            break
Msl = Reservoir()
# 0 board
# 1 st
# 2 at
# 3 action
# 4 all_actions
st = copy.deepcopy(temp[1])
board = copy.deepcopy(temp[0])
at = copy.deepcopy(temp[2])
action = [1, 6, 3, 4]
all_act = copy.deepcopy(temp[4])
st = np.array([st])
src, dst = supervised_learning(Msl=Msl, camp=camp_red, actions=all_act, sl_model=red_model, st=st)
print(src, "->", dst)

"""
board = generate_board()
board = list_to_string(board)
board = board.split(" ")
board = translate_message(board)
board = convert_board_to_array(board)
model = models.load_model("model.h5")
action = model.predict(board)
"""