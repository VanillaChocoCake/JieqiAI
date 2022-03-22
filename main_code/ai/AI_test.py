# 客户端
# AI主程序
import socket

from CircularBuffer import CircularBuffer
from RL import *
from Reservoir import Reservoir
from SL import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
red_sl_model = SLModel(camp=camp_red)
black_sl_model = SLModel(camp=camp_black)
red_agent = DQN(camp=camp_red)
black_agent = DQN(camp=camp_black)
Msl = Reservoir()
Mrl = CircularBuffer()
while True:
    turn = camp_red
    game_round = 0
    chess_num_now = chess_num_prev = 0
    no_eat_round = 0
    done = not_end
    while True:
        decision = None
        print("********************************")
        game_round += 1
        board_info = client.recv(2048)
        message = board_info.decode("utf-8").split(" ")
        board = translate_message(message)
        chess_num_now, red_chess_num, black_chess_num = chess_remain(board)
        if game_round == 1:
            chess_num_prev = chess_num_now
        elif chess_num_prev == chess_num_now:
            no_eat_round += 1
        elif chess_num_prev != chess_num_now:
            no_eat_round = 0
        print(board)
        print("回合：", game_round)
        print("剩余棋子数：", chess_num_now)
        print("红方剩余棋子数：", red_chess_num)
        print("黑方剩余棋子数：", black_chess_num)
        print("无吃子回合：", no_eat_round)
        red_actions, black_actions = available_actions(board)
        # 这里是决策
        ##################################################################
        # ct = 0 的情况，即episode terminated，困毙的局直接更新缓存，就不训练了 #
        ##################################################################
        if (game_round / 2 >= 500 or no_eat_round >= 40) and done == not_end:
            decision = "end"
            print("回合过多")
            done = end
        elif (len(red_actions) == 0 or len(black_actions) == 0) and done == not_end:
            decision = "end"
            done = end
            if len(red_actions) == 0:
                print("红方困毙")
            else:
                print("黑方困毙")
        ###########################################################
        # 强化学习与监督学习生成决策
        ###########################################################
        st = convert_board_to_array(board)
        if done == not_end and game_round > 1:
            # 将棋盘转换为10 * 9 * 16
            if turn == camp_red:
                beta_red = reinforcement_learning(Mrl=Mrl, camp=camp_red, dqn_agent=red_agent, st=st, actions=red_actions, batch_size=0)
                # 不知道为什么将train写在supervised_learning里面的时候模型会不训练，因此拿出来了
                # 因为save_count会根据存储次数而增加，当save_count为0的时候意味着已经增加了save_rate个元组
                # 为了避免过拟合，因此在此时进行训练一次
                pi_red = supervised_learning(camp=camp_red, sl_model=red_sl_model, st=st, actions=red_actions)
                sigma_red = (1 - eta) * pi_red + eta * beta_red
                plot(beta_red, pi_red, sigma_red)
                # sigma dim=8100
                action = np.argmax(sigma_red)
                # action 0 ~ 8099
                at = convert_num_to_array(action)
                # at dim=8100
                decision = convert_num_to_action(action)
                # decision string "a b c d"
            else:
                beta_black = reinforcement_learning(Mrl=Mrl, camp=camp_black, dqn_agent=black_agent, st=st, actions=black_actions, batch_size=0)
                pi_black = supervised_learning(camp=camp_black, sl_model=black_sl_model, st=st, actions=black_actions)
                sigma_black = (1 - eta) * pi_black + eta * beta_black
                plot(beta_black, pi_black, sigma_black)
                action = np.argmin(sigma_black)
                at = convert_num_to_array(action)
                decision = convert_num_to_action(action)
        if done == not_end and game_round == 1 and turn == camp_red:
            at = random_action(actions=red_actions)
            decision = convert_num_to_action(np.argmax(at))
        chess_num_prev = chess_num_now
        client.send(decision.encode("utf-8"))
        if decision == "end":
            break
        if turn == camp_red:
            turn = camp_black
        else:
            turn = camp_red
client.close()
