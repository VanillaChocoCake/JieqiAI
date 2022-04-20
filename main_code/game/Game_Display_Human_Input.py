import socket
import copy
from main_code.const import *

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
# port = 201
port = 2022
socket_server.bind((host, port))
socket_server.listen(5)
client_socket, address = socket_server.accept()
while True:
    human_side = int(input("人类：红方1，黑方0："))
    ai_side = 1 - human_side
    game_round = 1
    board = copy.deepcopy(initial_board)
    if human_side == camp_red:
        if game_round % 2 == 1:
            human_decision = input("人类决策：")
        else:

            ai_decision = client_socket.recv(2048).decode("utf-8")

