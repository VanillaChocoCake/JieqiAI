# as server
# 棋盘：
#   -------------y
#   |
#   |
#   |
#   x
# 从ai端接收4个数字，每个数字之间用空格隔开
# 例如收到“a b c d”，代表将(a, b)位置的棋子移到(c, d)位置
# 在游戏端并不考虑这个走法是否合理，所有的判断均在ai端完成\
# AI vs AI
# 强化学习训练用的游戏文件
import copy
import socket
import random
import time
from PIL import ImageGrab
from Game_Functions import *
from localtime import *
from const import *

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
# port = 201
port = 2022
socket_server.bind((host, port))
socket_server.listen(5)
client_socket, address = socket_server.accept()
Red_State = {"红车1": True, "红车2": True,
             "红炮1": True, "红炮2": True,
             "红马1": True, "红马2": True,
             "红相1": True, "红相2": True,
             "红仕1": True, "红仕2": True,
             "红兵1": True, "红兵2": True, "红兵3": True, "红兵4": True, "红兵5": True,
             "帅": False}
Black_State = {"黑车1": True, "黑车2": True,
               "黑炮1": True, "黑炮2": True,
               "黑马1": True, "黑马2": True,
               "黑象1": True, "黑象2": True,
               "黑士1": True, "黑士2": True,
               "黑卒1": True, "黑卒2": True, "黑卒3": True, "黑卒4": True, "黑卒5": True,
               "将": False}
# k-of-n encoding
while True:
    i = 0
    file_name = localtime()
    """all_movements = """""
    board = generate_board()
    red_info = copy.deepcopy(Red_State)
    black_info = copy.deepcopy(Black_State)
    human_side = int(input("人类：红方1，黑方0："))
    game_round = 0
    # 新建棋盘
    while True:
        i += 1
        """movement = """""
        game_round += 1
        chessboard = print_board(board, red_info, black_info)
        time.sleep(1)
        im = ImageGrab.grab()
        im.save(f"{i}.png")
        if human_side == camp_red:
            if game_round % 2 == 1:
                decision = input("人类决策：")
            else:
                message = list_to_string(chessboard)
                client_socket.send(message.encode("utf-8"))
                decision = client_socket.recv(2048).decode("utf-8")
        else:
            if game_round % 2 == 1:
                message = list_to_string(chessboard)
                client_socket.send(message.encode("utf-8"))
                decision = client_socket.recv(2048).decode("utf-8")
            else:
                decision = input("人类决策：")
        if decision == "end":
            print("本局结束")
            break
        decision = decision.split(" ")
        decision = list_to_int(decision)
        src = [decision[0], decision[1]]
        dst = [decision[2], decision[3]]
        # 更新棋盘开始
        board, red_info, black_info = update_board(src, dst, board, red_info, black_info)
        # time.sleep(5)
        """movement = f'[{src[0]},{src[1]},{dst[0]},{dst[1]}]'
        all_movements += f'{movement}, '
        with open(f'{file_name}.txt', "a+") as log:
            log.write(movement)"""
        # 更新棋盘结束
socket_server.close()


