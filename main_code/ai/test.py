# from AI_Functions import *
import numpy as np

from CircularBuffer import *
from SL import *
from const import *
"""
red_sl_model = SLModel(camp=camp_red)
black_sl_model = SLModel(camp=camp_black)
red_agent = DQN(camp=camp_red)
black_agent = DQN(camp=camp_black)
Msl = Reservoir()
Mrl = CircularBuffer()
red_agent.train(Mrl)
print(1)
"""
from SL import SLModel
from Reservoir import Reservoir
Msl = Reservoir()
rm = SLModel(camp=camp_red)
rm.train(Msl.red.st, Msl.red.at)
"""
# test
# red_model = SLModel(model=models.load_model("sl_model_red.h5"))
red_model = SLModel()
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
predict = red_model.predict(st)
available_policy = np.zeros(8100)
available_policy = convert_action_to_array(all_act, available_policy)
average_policy = select_best_action(predict, available_policy)
src, dst = convert_num_to_action(average_policy)
# src, dst = supervised_learning(Msl=Msl, camp=camp_red, actions=all_act, sl_model=red_model, st=st)
# print(src, "->", dst)
"""
"""
board = generate_board()
board = list_to_string(board)
board = board.split(" ")
board = translate_message(board)
board = convert_board_to_array(board)
model = models.load_model("model.h5")
action = model.predict(board)
"""
