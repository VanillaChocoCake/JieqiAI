# 客户端
# AI主程序
import copy
import socket
from AI_Functions import *
import numpy as np
from Reservoir import Reservoir
from CircularBuffer import CircularBuffer
from const import *
from SL import *
from RL import *
from tensorflow.keras import models
from tensorflow.keras.models import Model, Sequential


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 201
client.connect((host, port))
red_sl_model = SLModel(camp=camp_red)
black_sl_model = SLModel(camp=camp_black)
red_agent = DQN(camp=camp_red)
black_agent = DQN(camp=camp_black)
while True:
    turn = camp_red
    game_round = 0
    chess_num_now = chess_num_prev = 0
    no_eat_round = 0
    done = 1
    while True:
        print("********************************")
        game_round += 1
        board_info = client.recv(2048)
        message = board_info.decode("utf-8").split(" ")
        board = translate_message(message)
        chess_num_now, red_chess_num, black_chess_num = chess_remain(board)
        if game_round == 1:
            chess_num_prev = chess_num_now
        elif chess_num_prev == chess_num_now:
            no_eat_round += 1
        elif chess_num_prev != chess_num_now:
            no_eat_round = 0
        print(board)
        print("回合：", game_round)
        print("剩余棋子数：", chess_num_now)
        print("红方剩余棋子数：", red_chess_num)
        print("黑方剩余棋子数：", black_chess_num)
        print("无吃子回合：", no_eat_round)
        red_actions, black_actions = available_actions(board)
        # 这里是决策
        if game_round / 2 >= 500 or no_eat_round >= 40:
            decision = "end"
            print("回合过多")
            client.send(decision.encode("utf-8"))
            done = 0
            break
        if len(red_actions) == 0 or len(black_actions) == 0:
            decision = "end"
            if len(red_actions) == 0:
                print("红方困毙")
                reward = -1
            else:
                print("黑方困毙")
                reward = 1
            done = 0
            client.send(decision.encode("utf-8"))
            break
        if turn == camp_red:
            action = random.choice(red_actions)
            decision = str(action[0]) + " " + str(action[1]) + " " + str(action[2]) + " " + str(action[3])
            print("red:", decision)
        else:
            action = random.choice(black_actions)
            decision = str(action[0]) + " " + str(action[1]) + " " + str(action[2]) + " " + str(action[3])
            print("black:", decision)
        # 这里是决策结束
        st = convert_board_to_array(board)
        at = convert_action_to_array(action)
        if turn == camp_red:
            turn = camp_black
        else:
            turn = camp_red
        if decision == "end":
            break
        st_1 = st
        at_1 = at
        client.send(decision.encode("utf-8"))
        chess_num_prev = chess_num_now
client.close()

# TODO：AI核心代码
