# 展示代码，AI输入
import socket
from SL import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
red_sl_model = SLModel(camp=camp_red)
black_sl_model = SLModel(camp=camp_black)
while True:
    side = input("红方1，黑方0：")
    while True:
        board_info = client.recv(2048)
        message = board_info.decode("utf-8").split(" ")
        board = translate_message(message)
        if side == camp_red:

