# as client
import socket


def string_to_list(message):
    temp = []
    res = []
    for i in range(0, 10):
        temp.extend(message[9 * i: 9 * (i + 1)])
        res.append(temp)
        temp = []
    return res


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 201
client.connect((host, port))
while True:
    board_info = client.recv(2048)
    message = board_info.decode("utf-8")
    message = message.split(" ")
    board = string_to_list(message)
    print("棋盘：", board)
    decision = input("决策：")
    client.send(decision.encode("utf-8"))
    if decision == "end":
        # 打印最终的棋盘
        break
client.close()
