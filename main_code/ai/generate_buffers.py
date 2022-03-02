# as client
# 生成初始的Msl
import copy
import pickle
import random
import socket
import time

from AI_Functions import *
import numpy as np

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 2022
client.connect((host, port))
"""
while True:
    turn = camp_red
    game_round = 0
    chess_num_now = chess_num_prev = 0
    no_eat_round = 0
    done = 1
    while True:
        print("********************************")
        chess_num_now = 0
        red_chess_num = 0
        black_chesss_num = 0
        game_round += 1
        board_info = client.recv(2048)
        message = board_info.decode("utf-8").split(" ")
        board = translate_message(message)
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] != "空":
                    chess_num_now += 1
                    if camp(board[i][j]) == camp_red:
                        red_chess_num += 1
                    else:
                        black_chesss_num += 1
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
        print("黑方剩余棋子数：", black_chesss_num)
        print("无吃子回合：", no_eat_round)
        red_actions, black_actions = available_actions(board)
        # 这里是决策
        if game_round / 2 >= 500 or no_eat_round >= 40:
            decision = "end"
            print("回合过多")
            client.send(decision.encode("utf-8"))
            done = 0
            with open("Mrl_red.buf", "ab+") as Mrl_red:
                if game_round > 1:
                    res = [st_1, at_1, -1, st, done]
                    res = tuple(res)
                    pickle.dump(res, Mrl_red)
            with open("Mrl_black.buf", "ab+") as Mrl_black:
                if game_round > 1:
                    res = [st_1, at_1, 1, st, done]
                    res = tuple(res)
                    pickle.dump(res, Mrl_black)
            client.send(decision.encode("utf-8"))
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
            if turn == camp_red:
                with open("Mrl_red.buf", "ab+") as Mrl_red:
                    if game_round > 1 and done != 0:
                        res = [st_1, at_1, reward, st, done]
                        res = tuple(res)
                        pickle.dump(res, Mrl_red)
            else:
                with open("Mrl_black.buf", "ab+") as Mrl_black:
                    if game_round > 1 and done != 0:
                        res = [st_1, at_1, reward, st, done]
                        res = tuple(res)
                        pickle.dump(res, Mrl_black)
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
            with open("Msl_red.buf", "ab+") as Msl_red:
                num = random.uniform(0, 1)
                if num <= 0.2:
                    res = [st, at]
                    res = tuple(res)
                    pickle.dump(res, Msl_red)

            with open("Mrl_red.buf", "ab+") as Mrl_red:
                num = random.uniform(0, 1)
                if num <= 0.02 and game_round > 1:
                    res = [st_1, at_1, random.uniform(-1, 1), st, done]
                    res = tuple(res)
                    pickle.dump(res, Mrl_red)

            turn = camp_black
        else:
            with open("Msl_black.buf", "ab+") as Msl_black:
                num = random.uniform(0, 1)
                if num <= 0.2:
                    res = [st, at]
                    res = tuple(res)
                    pickle.dump(res, Msl_black)

            with open("Mrl_black.buf", "ab+") as Mrl_black:
                num = random.uniform(0, 1)
                if num <= 0.02 and game_round > 1:
                    res = [st_1, at_1, random.uniform(-1, 1), st, done]
                    res = tuple(res)
                    pickle.dump(res, Mrl_black)

            turn = camp_red
        if decision == "end":
            break
        st_1 = st
        at_1 = at
        client.send(decision.encode("utf-8"))
        chess_num_prev = chess_num_now
        # time.sleep(1)
client.close()
"""
while True:
    board_info = client.recv(2048)
    message = board_info.decode("utf-8").split(" ")
    board = translate_message(message)
    decision = input("decison:")
    client.send(decision.encode("utf-8"))
# TODO：AI核心代码
