# 基本上所有AI的函数都在这里面，有时间再写到class里
import copy
import numpy as np
from const import *
import random

normal_board = [["车", "马", "相", "仕", "帅", "仕", "相", "马", "车"],
                ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
                ["空", "炮", "空", "空", "空", "空", "空", "炮", "空"],
                ["兵", "空", "兵", "空", "兵", "空", "兵", "空", "兵"],
                ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
                ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
                ["卒", "空", "卒", "空", "卒", "空", "卒", "空", "卒"],
                ["空", "炮", "空", "空", "空", "空", "空", "炮", "空"],
                ["空", "空", "空", "空", "空", "空", "空", "空", "空"],
                ["车", "马", "象", "士", "将", "士", "象", "马", "车"]]
# (明棋7种+暗棋1种)*2+空=17种
# 棋盘 10 * 9
Chess_Dic = {"红车": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             "红炮": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             "红马": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             "红相": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             "红仕": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             "红兵": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             "帅": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             "红未": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             ##############################################################
             "黑车": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
             "黑炮": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
             "黑马": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
             "黑象": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
             "黑士": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
             "黑卒": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
             "将": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
             "黑未": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             ################################################################
             "空": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}


def translate_message(message):
    """
    将游戏端发过来的信息翻译为字符串的棋盘信息
    """
    temp = []
    res = []
    for i in range(0, 10):
        temp.extend(message[9 * i: 9 * (i + 1)])
        res.append(temp)
        temp = []
    return res


def convert_board_to_array(board):
    """
    将字符串的棋盘信息翻译为三维矩阵形式
    """
    res = copy.deepcopy(board)
    for i in range(0, 10):
        for j in range(0, 9):
            res[i][j] = Chess_Dic[board[i][j]]
    return np.array(res)


# 移动棋子，更新棋盘
def move_chess(board, src, dst):
    """
    :param board: 元素是字符串的棋盘
    :param src: 起始位置
    :param dst: 目标位置
    :return: 更新过后的棋盘
    """
    chess = board[src[0]][src[1]]
    board[src[0]][src[1]] = "空"
    board[dst[0]][dst[1]] = chess
    return board


# 检查棋子是哪个阵营的
def camp(chess):  # 判断棋子是哪一边的
    if chess.find('红') >= 0 or chess == "帅":  # 红
        return camp_red
    elif chess.find('黑') >= 0 or chess == "将":  # 黑
        return camp_black
    else:  # 空
        return blank


# 检查是否超出行动范围
def border_check(chess, target):
    """
    :param chess: 字符串形式的棋子
    :param target: 目标位置
    :return: 是否超越活动范围
    """
    if chess == "帅" or chess == "将":
        if (0 <= target[0] <= 2 and 3 <= target[1] <= 5) or (7 <= target[0] <= 9 and 3 <= target[1] <= 5):
            return safe
        else:
            return not safe
    else:
        if 0 <= target[0] <= 9 and 0 <= target[1] <= 8:
            return safe
        else:
            return not safe


# 在棋盘上找到目的棋子的位置
def find_chess(board, chess):
    """
    :param board: 元素是字符串的棋盘
    :param chess: 字符串的棋子
    :return: 是否找到
    """
    for x in range(0, 10):
        for y in range(0, 9):
            if board[x][y] == chess:
                return [x, y]


# 根据揭棋规则生成所有可行行动（士象可以过河）
def all_actions(board):
    """
    根据棋盘（字符串）信息，生成红方与黑方的所有行动（不考虑解将）
    :param board: 中文棋盘
    :return: 红黑行动
    """
    red_actions = []
    black_actions = []
    for x in range(0, 10):
        for y in range(0, 9):
            if board[x][y] == "空":
                continue
            chess = board[x][y]
            if chess.find('未') >= 0 and camp(chess) == 1:
                chess = "红" + normal_board[x][y]
            elif chess.find('未') >= 0 and camp(chess) == 0:
                chess = "黑" + normal_board[x][y]
            res = []
            if chess == "帅" or chess == "将":  # 帅或将只能上下左右走
                if border_check(chess, [x + 1, y]) is safe:
                    if camp(chess) != camp(board[x + 1][y]):
                        res.append([x, y, x + 1, y, chess])
                if border_check(chess, [x - 1, y]) is safe:
                    if camp(chess) != camp(board[x - 1][y]):
                        res.append([x, y, x - 1, y, chess])
                if border_check(chess, [x, y + 1]) is safe:
                    if camp(chess) != camp(board[x][y + 1]):
                        res.append([x, y, x, y + 1, chess])
                if border_check(chess, [x, y - 1]) is safe:
                    if camp(chess) != camp(board[x][y - 1]):
                        res.append([x, y, x, y - 1, chess])
            elif chess.find('士') >= 0 or chess.find('仕') >= 0:  # 仕或士只能一格对角线走
                if border_check(chess, [x - 1, y - 1]) is safe:
                    if camp(chess) != camp(board[x - 1][y - 1]):
                        res.append([x, y, x - 1, y - 1, chess])
                if border_check(chess, [x - 1, y + 1]) is safe:
                    if camp(chess) != camp(board[x - 1][y + 1]):
                        res.append([x, y, x - 1, y + 1, chess])
                if border_check(chess, [x + 1, y - 1]) is safe:
                    if camp(chess) != camp(board[x + 1][y - 1]):
                        res.append([x, y, x + 1, y - 1, chess])
                if border_check(chess, [x + 1, y + 1]) is safe:
                    if camp(chess) != camp(board[x + 1][y + 1]):
                        res.append([x, y, x + 1, y + 1, chess])
            elif chess.find('象') >= 0 or chess.find('相') >= 0:  # 相或象只能两格对角线走，还有塞象眼情况
                if border_check(chess, [x - 2, y - 2]) is safe:
                    if camp(chess) != camp(board[x - 2][y - 2]) and camp(board[x - 1][y - 1]) == blank:
                        res.append([x, y, x - 2, y - 2, chess])
                if border_check(chess, [x - 2, y + 2]) is safe:
                    if camp(chess) != camp(board[x - 2][y + 2]) and camp(board[x - 1][y + 1]) == blank:
                        res.append([x, y, x - 2, y + 2, chess])
                if border_check(chess, [x + 2, y - 2]) is safe:
                    if camp(chess) != camp(board[x + 2][y - 2]) and camp(board[x + 1][y - 1]) == blank:
                        res.append([x, y, x + 2, y - 2, chess])
                if border_check(chess, [x + 2, y + 2]) is safe:
                    if camp(chess) != camp(board[x + 2][y + 2]) and camp(board[x + 1][y + 1]) == blank:
                        res.append([x, y, x + 2, y + 2, chess])
            elif chess.find("车") >= 0:
                i = x - 1
                while border_check(chess, [i, y]) is safe:  # 上方所有可以走的点
                    if board[i][y] == "空":  # 空的当然可以走
                        res.append([x, y, i, y, chess])
                        i -= 1
                    elif camp(chess) != camp(board[i][y]):  # 吃棋子
                        res.append([x, y, i, y, chess])
                        break
                    else:  # 是同颜色的棋子
                        break
                i = x + 1
                while border_check(chess, [i, y]) is safe:  # 下方可以走的点
                    if board[i][y] == "空":
                        res.append([x, y, i, y, chess])
                        i += 1
                    elif camp(chess) != camp(board[i][y]):
                        res.append([x, y, i, y, chess])
                        break
                    else:
                        break
                j = y - 1
                while border_check(chess, [x, j]) is safe:  # 左边可以走的点
                    if board[x][j] == "空":
                        res.append([x, y, x, j, chess])
                        j -= 1
                    elif camp(chess) != camp(board[x][j]):
                        res.append([x, y, x, j, chess])
                        break
                    else:
                        break
                j = y + 1
                while border_check(chess, [x, j]) is safe:  # 右边可以走的点
                    if board[x][j] == "空":
                        res.append([x, y, x, j, chess])
                        j += 1
                    elif camp(chess) != camp(board[x][j]):
                        res.append([x, y, x, j, chess])
                        break
                    else:
                        break
            elif chess.find("炮") >= 0:
                i = x - 1
                jump = 0
                while border_check(chess, [i, y]) is safe:  # 上方所有可以走的点
                    if board[i][y] == "空" and jump == 0:  # 空的当然可以走
                        res.append([x, y, i, y, chess])
                    elif board[i][y] != "空" and jump == 0:  # 到达第一个棋子，准备看有没有吃子的可能
                        jump = 1
                    elif board[i][y] != "空" and jump == 1:  # 准备吃子后，有棋子
                        if camp(chess) != camp(board[i][y]):  # 是对方棋子就添加进去
                            res.append([x, y, i, y, chess])
                        break
                    i -= 1
                i = x + 1
                jump = 0
                while border_check(chess, [i, y]) is safe:  # 下方所有可以走的点
                    if board[i][y] == "空" and jump == 0:  # 空的当然可以走
                        res.append([x, y, i, y, chess])
                    elif board[i][y] != "空" and jump == 0:  # 到达第一个棋子，准备看有没有吃子的可能
                        jump = 1
                    elif board[i][y] != "空" and jump == 1:  # 准备吃子后，有棋子
                        if camp(chess) != camp(board[i][y]):  # 是对方棋子就添加进去
                            res.append([x, y, i, y, chess])
                        break
                    i += 1
                j = y - 1
                jump = 0
                while border_check(chess, [x, j]) is safe:  # 左方所有可以走的点
                    if board[x][j] == "空" and jump == 0:  # 空的当然可以走
                        res.append([x, y, x, j, chess])
                    elif board[x][j] != "空" and jump == 0:  # 到达第一个棋子，准备看有没有吃子的可能
                        jump = 1
                    elif board[x][j] != "空" and jump == 1:  # 准备吃子后，有对方棋子
                        if camp(chess) != camp(board[x][j]):
                            res.append([x, y, x, j, chess])
                        break
                    j -= 1
                j = y + 1
                jump = 0
                while border_check(chess, [x, j]) is safe:  # 右方所有可以走的点
                    if board[x][j] == "空" and jump == 0:  # 空的当然可以走
                        res.append([x, y, x, j, chess])
                    elif board[x][j] != "空" and jump == 0:  # 到达第一个棋子，准备看有没有吃子的可能
                        jump = 1
                    elif board[x][j] != "空" and jump == 1:  # 准备吃子后，有对方棋子
                        if camp(chess) != camp(board[x][j]):
                            res.append([x, y, x, j, chess])
                        break
                    j += 1
            elif chess.find("马") >= 0:
                if border_check(chess, [x + 1, y]) is safe:
                    if board[x + 1][y] == "空":  # 下方没有“蹩马腿”
                        if border_check(chess, [x + 2, y - 1]) is safe:
                            if camp(chess) != camp(board[x + 2][y - 1]):
                                res.append([x, y, x + 2, y - 1, chess])
                        if border_check(chess, [x + 2, y + 1]) is safe:
                            if camp(chess) != camp(board[x + 2][y + 1]):
                                res.append([x, y, x + 2, y + 1, chess])
                if border_check(chess, [x - 1, y]) is safe:
                    if board[x - 1][y] == "空":  # 上方没有“蹩马腿”
                        if border_check(chess, [x - 2, y - 1]) is safe:
                            if camp(chess) != camp(board[x - 2][y - 1]):
                                res.append([x, y, x - 2, y - 1, chess])
                        if border_check(chess, [x - 2, y + 1]) is safe:
                            if camp(chess) != camp(board[x - 2][y + 1]):
                                res.append([x, y, x - 2, y + 1, chess])
                if border_check(chess, [x, y - 1]) is safe:
                    if board[x][y - 1] == "空":  # 左方没有“蹩马腿”
                        if border_check(chess, [x - 1, y - 2]) is safe:
                            if camp(chess) != camp(board[x - 1][y - 2]):
                                res.append([x, y, x - 1, y - 2, chess])
                        if border_check(chess, [x + 1, y - 2]) is safe:
                            if camp(chess) != camp(board[x + 1][y - 2]):
                                res.append([x, y, x + 1, y - 2, chess])
                if border_check(chess, [x, y + 1]) is safe:
                    if board[x][y + 1] == "空":  # 右方没有“蹩马腿”
                        if border_check(chess, [x - 1, y + 2]) is safe:
                            if camp(chess) != camp(board[x - 1][y + 2]):
                                res.append([x, y, x - 1, y + 2, chess])
                        if border_check(chess, [x + 1, y + 2]) is safe:
                            if camp(chess) != camp(board[x + 1][y + 2]):
                                res.append([x, y, x + 1, y + 2, chess])
            elif chess.find("兵") >= 0:  # 红兵分别在下面和上面的情况
                black_king = find_chess(board, "将")
                if black_king[0] <= 2:
                    if border_check(chess, [x - 1, y]) is safe:
                        if camp(chess) != camp(board[x - 1][y]):
                            res.append([x, y, x - 1, y, chess])
                    if 0 <= x <= 4:
                        if border_check(chess, [x, y - 1]) is safe:
                            if camp(chess) != camp(board[x][y - 1]):
                                res.append([x, y, x, y - 1, chess])
                        if border_check(chess, [x, y + 1]) is safe:
                            if camp(chess) != camp(board[x][y + 1]):
                                res.append([x, y, x, y + 1, chess])
                elif black_king[0] >= 7:
                    if border_check(chess, [x + 1, y]) is safe:
                        if camp(chess) != camp(board[x + 1][y]):
                            res.append([x, y, x + 1, y, chess])
                    if 5 <= x <= 9:
                        if border_check(chess, [x, y - 1]) is safe:
                            if camp(chess) != camp(board[x][y - 1]):
                                res.append([x, y, x, y - 1, chess])
                        if border_check(chess, [x, y + 1]) is safe:
                            if camp(chess) != camp(board[x][y + 1]):
                                res.append([x, y, x, y + 1, chess])
            elif chess.find("卒") >= 0:
                red_king = find_chess(board, "帅")
                if red_king[0] <= 2:
                    if border_check(chess, [x - 1, y]) is safe:
                        if camp(chess) != camp(board[x - 1][y]):
                            res.append([x, y, x - 1, y, chess])
                    if 0 <= x <= 4:
                        if border_check(chess, [x, y - 1]) is safe:
                            if camp(chess) != camp(board[x][y - 1]):
                                res.append([x, y, x, y - 1, chess])
                        if border_check(chess, [x, y + 1]) is safe:
                            if camp(chess) != camp(board[x][y + 1]):
                                res.append([x, y, x, y + 1, chess])
                elif red_king[0] >= 7:
                    if border_check(chess, [x + 1, y]) is safe:
                        if camp(chess) != camp(board[x + 1][y]):
                            res.append([x, y, x + 1, y, chess])
                    if 5 <= x <= 9:
                        if border_check(chess, [x, y - 1]) is safe:
                            if camp(chess) != camp(board[x][y - 1]):
                                res.append([x, y, x, y - 1, chess])
                        if border_check(chess, [x, y + 1]) is safe:
                            if camp(chess) != camp(board[x][y + 1]):
                                res.append([x, y, x, y + 1, chess])
            if camp(chess) == camp_red:
                red_actions.extend(res)
            else:
                black_actions.extend(res)
    return red_actions, black_actions


# 检查目前是否有将军的情况
def checkmate(red_king, black_king, red_actions, black_actions):
    """
    根据红黑方的帅/将位置与红黑放的所有行动，判断是否有将军行为
    :param red_king: 帅位置
    :param black_king: 将位置
    :param red_actions: 红方所有行动
    :param black_actions: 黑方所有行动
    :return: 是否有将军的情况
    """
    res = []
    for red_action in red_actions:
        if black_king == [red_action[2], red_action[3]]:  # 红 将军 黑
            res.append(red_check_black)
            break
    for black_action in black_actions:
        if red_king == [black_action[2], black_action[3]]:  # 黑 将军 红
            res.append(black_check_red)
            break
    if res == [red_check_black]:
        return red_check_black
    elif res == [black_check_red]:
        return black_check_red
    elif res == [red_check_black, black_check_red]:
        return not_available
    else:
        return not_check


# 生成所有双方合法可行的行动（送将等行为视为违反规则，因此做了处理），无可行行动视为困毙
# 另外根据规则，被将军需要解将，因此只保留解将的行动，无法解将视为将死，在函数逻辑里等同于困毙
def available_actions(board):
    """
    根据红黑方的所有行动与将军情况，筛选出所有合法的行动
    :param board: 中文棋盘
    :return: 红黑方所有合法行动，合法行动数目为0意味着困毙/无法解将
    """
    red_actions, black_actions = all_actions(board)
    red_king = find_chess(board, "帅")
    black_king = find_chess(board, "将")
    red_actions_modified = []
    black_actions_modified = []
    ######################################################
    # 不要把将/帅移到被将军的位置（炮位置的除外）#
    ######################################################
    red_king_move = []
    black_king_move = []
    for action in red_actions:
        if action[4] == "帅":
            red_king_move.append(action)
    for action in black_actions:
        if action[4] == "将":
            black_king_move.append(action)
    for move in red_king_move:
        for action in black_actions:
            if [action[2], action[3]] == [move[2], move[3]] and action[4].find("炮") < 0:
                red_actions.remove(move)
                break
    for move in black_king_move:
        for action in red_actions:
            if [action[2], action[3]] == [move[2], move[3]] and action[4].find("炮") < 0:
                black_actions.remove(move)
                break
    ######################################################
    # 不要把棋子移到会被将军的位置 #
    ######################################################
    ra_temp = copy.deepcopy(red_actions)
    ba_temp = copy.deepcopy(black_actions)
    for action in red_actions:
        temp_board = copy.deepcopy(board)
        temp_board = move_chess(temp_board, [action[0], action[1]], [action[2], action[3]])
        temp_red_king = find_chess(temp_board, "帅")
        temp_black_king = find_chess(temp_board, "将")
        try:
            temp_red_actions, temp_black_actions = all_actions(temp_board)
        except:  # 进入except说明在move_chess那里已经把将/帅吃掉了，这就说明处于将军状态，留给下个部分处理
            continue
        check_res = checkmate(temp_red_king, temp_black_king, temp_red_actions, temp_black_actions)
        if check_res == black_check_red or check_res == not_available:
            ra_temp.remove(action)
    red_actions = copy.deepcopy(ra_temp)
    for action in black_actions:
        temp_board = copy.deepcopy(board)
        temp_board = move_chess(temp_board, [action[0], action[1]], [action[2], action[3]])
        temp_red_king = find_chess(temp_board, "帅")
        temp_black_king = find_chess(temp_board, "将")
        try:
            temp_red_actions, temp_black_actions = all_actions(temp_board)
        except:
            continue
        check_res = checkmate(temp_red_king, temp_black_king, temp_red_actions, temp_black_actions)
        if check_res == red_check_black or check_res == not_available:
            ba_temp.remove(action)
    black_actions = copy.deepcopy(ba_temp)
    check_res = checkmate(red_king, black_king, red_actions, black_actions)
    if check_res == red_check_black or check_res == not_available:  # 黑被将军
        # 在得知被将军后，先模拟实施一遍自己所有的行动，将实施后的棋盘输入到checkmate中检验，
        # 如果不再被将军，则为可行行动，其余行动均删除
        for action in black_actions:  # 找到”解将“的走法
            if [action[2], action[3]] == red_king:
                continue
            temp_board = copy.deepcopy(board)
            temp_board = move_chess(temp_board, [action[0], action[1]], [action[2], action[3]])  # 从可行行动中按顺序选取更新棋盘
            temp_red_actions, temp_black_actions = all_actions(temp_board)
            temp_red_king = find_chess(temp_board, "帅")
            temp_black_king = find_chess(temp_board, "将")
            check_res = checkmate(temp_red_king, temp_black_king, temp_red_actions, temp_black_actions)
            if check_res == not_check or check_res == black_check_red:
                black_actions_modified.append(action)
        red_actions_modified = copy.deepcopy(red_actions)
    elif check_res == black_check_red or check_res == not_available:  # 红被将军
        for action in red_actions:  # 找到”解将“的走法
            if [action[2], action[3]] == black_king:
                continue
            temp_board = copy.deepcopy(board)
            temp_board = move_chess(temp_board, [action[0], action[1]], [action[2], action[3]])  # 从可行行动中按顺序选取更新棋盘
            temp_red_actions, temp_black_actions = all_actions(temp_board)
            temp_red_king = find_chess(temp_board, "帅")
            temp_black_king = find_chess(temp_board, "将")
            check_res = checkmate(temp_red_king, temp_black_king, temp_red_actions, temp_black_actions)
            if check_res == not_check or check_res == red_check_black:
                red_actions_modified.append(action)
        black_actions_modified = copy.deepcopy(black_actions)
    else:
        red_actions_modified = copy.deepcopy(red_actions)
        black_actions_modified = copy.deepcopy(black_actions)
    if red_king[1] != black_king[1]:  # 双方的将/帅在不同列
        no_other_chess = 1
        if red_king[0] > black_king[0]:  # 避免照将的情况，先修剪红色方，再修剪黑色方
            for i in range(black_king[0] + 1, red_king[0]):
                if board[i][black_king[1]] != "空":
                    no_other_chess = 0
                    break
        else:
            for i in range(red_king[0] + 1, black_king[0]):
                if board[i][black_king[1]] != "空":
                    no_other_chess = 0
                    break
        if no_other_chess:
            try:
                red_actions_modified.remove([red_king[0], red_king[1], red_king[0], black_king[1], "帅"])
            except:
                pass
        no_other_chess = 1
        if red_king[0] > black_king[0]:  # 避免照将的情况，先修剪红色方，再修剪黑色方
            for i in range(black_king[0] + 1, red_king[0]):
                if board[i][red_king[1]] != "空":
                    no_other_chess = 0
                    break
        else:
            for i in range(red_king[0] + 1, black_king[0]):
                if board[i][red_king[1]] != "空":
                    no_other_chess = 0
                    break
        if no_other_chess:
            try:
                black_actions_modified.remove([black_king[0], black_king[1], black_king[0], red_king[1], "将"])
            except:
                pass
    red_temp = copy.deepcopy(red_actions_modified)
    black_temp = copy.deepcopy(black_actions_modified)
    red_actions_modified = []
    black_actions_modified = []
    for action in red_temp:
        red_actions_modified.append(
            [action[0], action[1], action[2], action[3], Chess_Dic[board[action[0]][action[1]]]])
    for action in black_temp:
        black_actions_modified.append(
            [action[0], action[1], action[2], action[3], Chess_Dic[board[action[0]][action[1]]]])
    return red_actions_modified, black_actions_modified


# 棋盘形状：红方在上
def convert_action_to_array(action, available_action_array=None):
    """
    将行动转换为one-hot编码或者更新可行行动数列
    :param available_action_array: 可行行动数列
    :param action:行动
    :return:数列
    """
    res = np.zeros(8100)
    if available_action_array is None:
        src = [action[0], action[1]]
        dst = [action[2], action[3]]
        res[90 * (9 * src[0] + src[1]) + 9 * dst[0] + dst[1]] = 1
    else:
        for a in action:
            src = [a[0], a[1]]
            dst = [a[2], a[3]]
            res[90 * (9 * src[0] + src[1]) + 9 * dst[0] + dst[1]] = 1
    return res


def convert_num_to_action(num):
    """
    num: 下标(0 ~ 8099)
    return: string "a b c d"
    """
    src = [0, 0]
    dst = [0, 0]
    src[0] = int(int(num / 90) / 9)
    src[1] = int(num / 90) - 9 * src[0]
    dst[0] = int((num - 90 * int(num / 90)) / 9)
    dst[1] = num - 90 * int(num / 90) - 9 * dst[0]
    return str(src[0]) + " " + str(src[1]) + " " + str(dst[0]) + " " + str(dst[1])


def generate_policy(predict_res, available_actions):
    """
    将输出结果中的不可行行动排除，随后进行归一化
    :param predict_res:模型输出的结果，8100维
    :param available_actions:可行行动，8100维
    :return:8100维数列
    """

    def normalization(arr):
        base = np.max(abs(arr))
        return arr / base

    for i in range(0, len(predict_res)):
        predict_res[i] = predict_res[i] * available_actions[i]
    predict_res = normalization(predict_res)
    return predict_res


def chess_remain(board):
    chess_num_now = 0
    red_chess_num = 0
    black_chess_num = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] != "空":
                chess_num_now += 1
                if camp(board[i][j]) == camp_red:
                    red_chess_num += 1
                else:
                    black_chess_num += 1
    return chess_num_now, red_chess_num, black_chess_num


def random_action(actions):
    """
    actions: [a, b, c, d, e]
    return: dim=8100
    """
    random_policy = random.sample(actions, 1)[0]
    random_policy = convert_action_to_array(random_policy)
    return random_policy


def convert_num_to_array(num):
    """
    num: 下标
    return: dim=8100
    """
    arr = np.zeros(8100)
    arr[num] = 1
    return arr
