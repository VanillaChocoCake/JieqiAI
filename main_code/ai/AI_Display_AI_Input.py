# 展示代码，AI输入
import socket
from SL import *
import numpy as np

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
red_sl_model = SLModel(camp=camp_red)
black_sl_model = SLModel(camp=camp_black)
while True:
    side = input("红方1，黑方0：")
    while True:
        board_info = client.recv(2048)
        message = board_info.decode("utf-8")
        if message == "end":
            break
        message = message.split(" ")
        board = translate_message(message)
        st = convert_board_to_array(board)
        if side == camp_red:
            predict = red_sl_model.predict(st)
            action = np.argmax(predict)
        else:
            predict = black_sl_model.predict(st)
            action = np.argmin(message)
        decision = convert_board_to_array(action)
        client.send(decision.encode("utf-8"))


