# 展示代码，AI输入
import socket
from SL import *
import numpy as np
from AI_Functions import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
red_sl_model = SLModel(camp=camp_red)
black_sl_model = SLModel(camp=camp_black)
while True:
    side = int(input("AI:红方1，黑方0："))
    while True:
        board_info = client.recv(2048)
        message = board_info.decode("utf-8")
        message = message.split(" ")
        board = translate_message(message)
        st = convert_board_to_array(board)
        red_actions, black_actions = available_actions(board)
        if side == camp_red:
            predict = supervised_learning(camp=camp_red, sl_model=red_sl_model, st=st, actions=red_actions)
            action = np.argmax(predict)
        else:
            predict = supervised_learning(camp=camp_black, sl_model=black_sl_model, st=st, actions=black_actions)
            action = np.argmin(message)
        decision = convert_num_to_action(action)
        client.send(decision.encode("utf-8"))


