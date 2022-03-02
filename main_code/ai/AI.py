# 客户端
# AI主程序
import copy
import socket
from AI_Functions import *
import numpy as np
from Reservoir import Reservoir
from CircularBuffer import CircularBuffer
from const import *
from SL import SLModel
from tensorflow.keras import models


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 201
client.connect((host, port))
red_sl_model = SLModel()
black_sl_model = SLModel()
while True:
    game_round = 0
    while True:
        game_round += 1
        board_info = client.recv(2048)
        message = board_info.decode("utf-8").split(" ")
        board = translate_message(message)
        print("棋盘：", board)
        # 这里是决策

        if game_round > 250:
            decision = "end"
        else:
            decision = input("决策：")

        # 这里是决策结束
        client.send(decision.encode("utf-8"))
        if decision == "end":
            print("本局结束")
            break
        elif decision == "quit":
            print("终止")
            break
    if decision == "quit":
        break
client.close()

# TODO：AI核心代码
