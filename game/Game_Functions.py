import random

Red_Chess = ["红车1", "红车2", "红炮1", "红炮2", "红马1", "红马2", "红相1", "红相2", "红仕1", "红仕2", "红兵1", "红兵2", "红兵3", "红兵4", "红兵5"]
Black_Chess = ["黑车1", "黑车2", "黑炮1", "黑炮2", "黑马1", "黑马2", "黑象1", "黑象2", "黑士1", "黑士2", "黑卒1", "黑卒2", "黑卒3", "黑卒4", "黑卒5"]
Red_King = "帅"
Black_King = "将"


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


def camp(chess):  # 判断棋子是哪一边的
    if chess.find('红') >= 0 or chess == "帅":
        return 1
    elif chess.find('黑') >= 0 or chess == "将":
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
    """
    :param board: 棋盘
    :param red_info: 红方棋子的可见信息
    :param black_info: 黑方棋子的可见信息
    :return: 打印棋盘
    """
    print("*******************************")
    temp = []
    res = []
    print("  零  一  二  三  四  五  六  七  八")
    for i in range(0, 10):
        line = board[i]
        print(f'{i} ', end="")
        for j in range(0, 9):
            real_name = chess = line[j]
            if camp(chess) == 1 and red_info[chess] is False:
                chess = "".join([letter for letter in chess if letter != "红"])
                chess = "".join([letter for letter in chess if not letter.isdigit()])
                print(red_string(chess), " ", end="")
                temp.append(real_name)
            elif camp(chess) == 1 and red_info[chess] is True:
                print(red_hidden_string("未"), " ", end="")
                temp.append("红未")
            elif camp(chess) == 0 and black_info[chess] is False:
                chess = "".join([letter for letter in chess if letter != "黑"])
                chess = "".join([letter for letter in chess if not letter.isdigit()])
                print(black_string(chess), " ", end="")
                temp.append(real_name)
            elif camp(chess) == 0 and black_info[chess] is True:
                print(black_hidden_string("未"), " ", end="")
                temp.append("黑未")
            else:
                print(chess, " ", end="")
                temp.append(chess)
            if j == 8:
                print("\n")
        res.append(temp)
        temp = []
    return res


def list_to_string(board):
    """
    :param board: 棋盘
    :return: 将棋盘翻译为字符串，发送到AI端
    """
    res = ""
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if i == len(board) - 1 and j == len(board[i]) - 1:
                res = res + board[i][j]
            else:
                res = res + board[i][j] + " "
    res = "".join([letter for letter in res if not letter.isdigit()])
    return res


def update_board(src, dst, board, red_info, black_info):
    src_chess = board[src[0]][src[1]]
    board[dst[0]][dst[1]] = src_chess
    board[src[0]][src[1]] = "空"
    if camp(src_chess) == 1:
        red_info[src_chess] = False
    elif camp(src_chess) == 0:
        black_info[src_chess] = False
    return board, red_info, black_info


def list_to_int(lst):
    for i in range(0, len(lst)):
        lst[i] = int(lst[i])
    return lst
