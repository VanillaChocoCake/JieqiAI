import socket
import copy
from main_code.const import *
from main_code.game.Game_Functions import *
from main_code.localtime import localtime
# 棋盘翻转
Red_Dic = {'1': "红车",
           '2': "红炮",
           '3': "红马",
           '4': "红相",
           '5': "红仕",
           '6': "红兵"}
Black_Dic = {'1': "黑车",
             '2': "黑炮",
             '3': "黑马",
             '4': "黑象",
             '5': "黑士",
             '6': "黑卒"}


def update_display_board(src, dst, board, camp, chess=None):
    src_chess = board[src[0]][src[1]]
    if chess is not None:
        if camp == camp_red:
            src_chess = Red_Dic[chess]
        else:
            src_chess = Black_Dic[chess]
    board[dst[0]][dst[1]] = src_chess
    board[src[0]][src[1]] = "空"
    return board


initial_board = [['红未', '红未', '红未', '红未', '帅', '红未', '红未', '红未', '红未'],
                 ['空', '空', '空', '空', '空', '空', '空', '空', '空'],
                 ['空', '红未', '空', '空', '空', '空', '空', '红未', '空'],
                 ['红未', '空', '红未', '空', '红未', '空', '红未', '空', '红未'],
                 ['空', '空', '空', '空', '空', '空', '空', '空', '空'],
                 ['空', '空', '空', '空', '空', '空', '空', '空', '空'],
                 ['黑未', '空', '黑未', '空', '黑未', '空', '黑未', '空', '黑未'],
                 ['空', '黑未', '空', '空', '空', '空', '空', '黑未', '空'],
                 ['空', '空', '空', '空', '空', '空', '空', '空', '空'],
                 ['黑未', '黑未', '黑未', '黑未', '将', '黑未', '黑未', '黑未', '黑未']]
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 2022
socket_server.bind((host, port))
socket_server.listen(5)
client_socket, address = socket_server.accept()
file_name = localtime()
while True:
    human_side = int(input("人类：红方1，黑方0："))
    ai_side = 1 - human_side
    game_round = 1
    board = copy.deepcopy(initial_board)
    all_movements = ""
    if human_side == camp_red:
        if game_round % 2 == 1:
            for key in Red_Dic:
                print(f'{key}-{Red_Dic[key]}')
            human_decision = input("人类决策：").split(" ")
            src = [int(human_decision[0]), int(human_decision[1])]
            dst = [int(human_decision[2]), int(human_decision[2])]
            print(src, dst)
            if len(human_decision) == 5:
                board = update_display_board(src, dst, board, camp_red, chess=human_decision[4])
            else:
                board = update_display_board(src, dst, board, camp_red)
        else:
            message = list_to_string(board)
            client_socket.send(message.encode("utf-8"))
            ai_decision = client_socket.recv(2048).decode("utf-8").split(" ")
            src = [int(ai_decision[0]), int(ai_decision[1])]
            dst = [int(ai_decision[2]), int(ai_decision[3])]
            print(src, dst)
            board = update_display_board(src, dst, board, camp_black)
            if board[dst[0]][dst[1]] == "黑未":
                for key in Black_Dic:
                    print(f'{key}-{Black_Dic[key]}')
                chess = input("该棋子揭开为：")
                board[dst[0]][dst[1]] = Black_Dic[chess]
        all_movements += f'[{src[0]},{src[1]},{dst[0]},{dst[1]}]'

