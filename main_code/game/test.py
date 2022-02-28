# as server
# 棋盘：
#   -------------y
#   |
#   |
#   |
#   x
# 从ai端接收4个数字，每个数字之间用空格隔开
# 例如收到“a b c d”，代表将(a, b)位置的棋子移到(c, d)位置
# 在游戏端并不考虑这个走法是否合理，所有的判断均在ai端完成
import socket
import random

Red_Chess = ["红车1", "红车2", "红炮1", "红炮2", "红马1", "红马2", "红相1", "红相2", "红仕1", "红仕2", "红兵1", "红兵2", "红兵3", "红兵4", "红兵5"]
Black_Chess = ["黑车1", "黑车2", "黑炮1", "黑炮2", "黑马1", "黑马2", "黑象1", "黑象2", "黑士1", "黑士2", "黑卒1", "黑卒2", "黑卒3", "黑卒4", "黑卒5"]
Red_King = "帅"
Black_King = "将"
Red_Dic = {"红车1": True, "红车2": True, "红炮1": True, "红炮2": True, "红马1": True, "红马2": True, "红相1": True, "红相2": True,
           "红仕1": True, "红仕2": True, "红兵1": True, "红兵2": True, "红兵3": True, "红兵4": True, "红兵5": True, "帅": False}
Black_Dic = {"黑车1": True, "黑车2": True, "黑炮1": True, "黑炮2": True, "黑马1": True, "黑马2": True, "黑象1": True, "黑象2": True,
             "黑士1": True, "黑士2": True, "黑卒1": True, "黑卒2": True, "黑卒3": True, "黑卒4": True, "黑卒5": True, "将": False}


def generate_red(board, chess_set):  # 在棋盘上生成红色方棋子
    for y in range(0, 9):
        if y == 4:
            continue
        else:
            chess = chess_set[0]
            board[0][y] = chess
            chess_set.remove(chess)
    board[0][4] = Red_King
    for y in range(0, 5):
        chess = chess_set[0]
        board[3][2 * y] = chess
        chess_set.remove(chess)
    board[2][1] = chess_set[0]
    board[2][7] = chess_set[1]
    return board


def generate_black(board, chess_set):  # 棋盘上生成黑色方棋子
    for y in range(0, 9):
        if y == 4:
            continue
        else:
            chess = chess_set[0]
            board[9][y] = chess
            chess_set.remove(chess)
    board[9][4] = Black_King
    for y in range(0, 5):
        chess = chess_set[0]
        board[6][2 * y] = chess
        chess_set.remove(chess)
    board[7][1] = chess_set[0]
    board[7][7] = chess_set[1]
    return board


def generate_board():  # 生成初始棋盘
    board = [["空", "空", "空", "空", "空", "空", "空", "空", "空"],
             ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
             ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
             ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
             ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
             ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
             ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
             ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
             ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
             ["空", "空", "空", "空", "空", "空", "空", "空", "空"]]
    red_set = Red_Chess[:]
    black_set = Black_Chess[:]
    random.shuffle(red_set)
    random.shuffle(black_set)
    generate_red(board, red_set)
    generate_black(board, black_set)
    return board


def isred(chess):  # 判断棋子是哪一边的
    if chess.find('红') == 0 or chess == "帅":
        return 1
    elif chess.find('黑') == 0 or chess == "将":
        return 0
    else:
        return -1


def red_string(sentence):  # 红色已知棋子的颜色
    return "\033[1;31;49m" + sentence + "\033[0m"


def black_string(sentence):  # 黑色已知棋子的颜色
    return "\033[1;30;49m" + sentence + "\033[0m"


def red_hidden_string(sentence):  # 红色未知棋子的颜色
    return "\033[1;35;49m" + sentence + "\033[0m"


def black_hidden_string(sentence):  # 黑色未知棋子的颜色
    return "\033[1;36;49m" + sentence + "\033[0m"


def print_board(board, red_info, black_info):  # red_info与black_info指棋盘上的已知棋子与未知棋子的信息
    temp = []
    res = []
    for i in range(0, 10):
        line = board[i]
        for j in range(0, 9):
            real_name = chess = line[j]
            if isred(chess) == 1 and red_info[chess] is False:
                try:
                    chess = chess.replace("红", "")
                except:
                    pass
                try:
                    chess = chess.replace("1", "")
                except:
                    pass
                try:
                    chess = chess.replace("2", "")
                except:
                    pass
                try:
                    chess = chess.replace("3", "")
                except:
                    pass
                try:
                    chess = chess.replace("4", "")
                except:
                    pass
                try:
                    chess = chess.replace("5", "")
                except:
                    pass
                print(red_string(chess), " ", end="")
                temp.append(real_name)
            elif isred(chess) == 1 and red_info[chess] is True:
                print(red_hidden_string("未"), " ", end="")
                temp.append("红未")
            elif isred(chess) == 0 and black_info[chess] is False:
                try:
                    chess = chess.replace("黑", "")
                except:
                    pass
                try:
                    chess = chess.replace("1", "")
                except:
                    pass
                try:
                    chess = chess.replace("2", "")
                except:
                    pass
                try:
                    chess = chess.replace("3", "")
                except:
                    pass
                try:
                    chess = chess.replace("4", "")
                except:
                    pass
                try:
                    chess = chess.replace("5", "")
                except:
                    pass
                print(black_string(chess), " ", end="")
                temp.append(real_name)
            elif isred(chess) == 0 and black_info[chess] is True:
                print(black_hidden_string("未"), " ", end="")
                temp.append("黑未")
            else:
                print(chess, " ", end="")
                temp.append(chess)
            if j == 8:
                print("\n")
        res.append(temp)
        temp = []
    print("*******************************")
    return res


def list_to_string(board):
    res = ""
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if i == len(board) - 1 and j == len(board[i]) - 1:
                res = res + board[i][j]
            else:
                res = res + board[i][j] + " "
    return res


def update_board(src, dst, board, red_info, black_info):
    src_chess = board[src[0]][src[1]]
    board[dst[0]][dst[1]] = src_chess
    board[src[0]][src[1]] = "空"
    if isred(src_chess) == 1:
        red_info[src_chess] = False
    elif isred(src_chess) == 0:
        black_info[src_chess] = False
    return board, red_info, black_info


while True:
    board = generate_board()
    red_info = Red_Dic.copy()
    black_info = Black_Dic.copy()
    # 新建棋盘
    while True:
        chessboard = print_board(board, red_info, black_info)
        print(chessboard)
        message = list_to_string(chessboard)
        decision = input("decision:").split(" ")
        for i in range(0, len(decision)):
            decision[i] = int(decision[i])
        src = [decision[0], decision[1]]
        dst = [decision[2], decision[3]]
        print("决策：", decision)
        if decision == "end" or decision == "quit":
            break
        # 更新棋盘开始
        board, red_info, black_info = update_board(src, dst, board, red_info, black_info)
        # 更新棋盘结束
    if decision == "quit":
        break

# todo: 终局
