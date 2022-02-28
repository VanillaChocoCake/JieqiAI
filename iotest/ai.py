# as client
import socket
from main_code.ai.AI_Functions import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
# port = 201
port = 2022
client.connect((host, port))
while True:
    board_info = client.recv(2048)
    message = board_info.decode("utf-8")
    message = message.split(" ")
    board = translate_message(message)
    print("棋盘：", board)
    decision = input("决策：")
    client.send(decision.encode("utf-8"))
    if decision == "end":
        # 打印最终的棋盘
        break
client.close()
