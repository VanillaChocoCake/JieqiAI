# as server
import socket


def list_to_string(board):
    res = ""
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if i == len(board) - 1 and j == len(board[i]) - 1:
                res = res + board[i][j]
            else:
                res = res + board[i][j] + " "
    return res


board_info = [["空", "空", "空", "空", "空", "空", "空", "空", "空"],
              ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
              ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
              ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
              ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
              ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
              ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
              ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
              ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
              ["空", "空", "空", "空", "空", "空", "空", "空", "空"]]
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 201
socket_server.bind((host, port))
socket_server.listen(5)
client_socket, address = socket_server.accept()
client_socket_1, address_1 = socket_server.accept()
i = 0
while True:
    message = list_to_string(board_info)
    # board_info = input("棋盘信息：")
    if i == 0:
        client_socket.send(message.encode("utf-8"))
        decision = client_socket.recv(2048)
        decision = decision.decode("utf-8").split(" ")
        for i in range(0, len(decision)):
            decision[i] = int(decision[i])
        print("决策：", decision)
        i = 1
    else:
        client_socket_1.send(message.encode("utf-8"))
        decision = client_socket_1.recv(2048)
        decision = decision.decode("utf-8").split(" ")
        for i in range(0, len(decision)):
            decision[i] = int(decision[i])
        print("决策：", decision)
        i = 0
    if decision == "end":
        break
socket_server.close()
