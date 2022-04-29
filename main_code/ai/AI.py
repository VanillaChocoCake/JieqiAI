# 客户端
# AI主程序
import random
import socket
from CircularBuffer import CircularBuffer
from RL import *
from Reservoir import Reservoir
from SL import *
from AI_Functions import *

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
        if (game_round / 2 >= 500 or no_eat_round >= 30) and done == not_end:
            decision = "end"
            print("回合过多")
            done = end
        elif (len(red_actions) == 0 or len(black_actions) == 0) and done == not_end:
            decision = "end"
            done = end
            if len(red_actions) == 0:
                print("红方困毙")
                reward = black_win
                if turn == camp_red:
                    tup_red = (st_2, at_2, reward, st_1, done)
                    Mrl.update(tup=tup_red, camp=camp_red)
                    tup_black = (st_1, at_1, reward, st, done)
                    Mrl.update(tup_black, camp=camp_black)
                else:
                    tup_red = (st_1, at_1, reward, st, done)
                    Mrl.update(tup=tup_red, camp=camp_red)
                    tup_black = (st_2, at_2, reward, st_1, done)
                    Mrl.update(tup_black, camp=camp_black)
            else:
                print("黑方困毙")
                reward = red_win
                if turn == camp_red:
                    tup_red = (st_1, at_1, reward, st, done)
                    Mrl.update(tup=tup_red, camp=camp_red)
                    tup_black = (st_2, at_2, reward, st_1, done)
                    Mrl.update(tup_black, camp=camp_black)
                else:
                    tup_red = (st_1, at_1, reward, st, done)
                    Mrl.update(tup=tup_red, camp=camp_red)
                    tup_black = (st_2, at_2, reward, st_1, done)
                    Mrl.update(tup_black, camp=camp_black)
        ###########################################################
        # 强化学习与监督学习生成决策
        ###########################################################
        st = convert_board_to_array(board)
        if done == not_end and game_round > 1:
            # 将棋盘转换为10 * 9 * 16
            if turn == camp_red:
                beta_red = reinforcement_learning(Mrl=Mrl, camp=camp_red, dqn_agent=red_agent, st=st, actions=red_actions, batch_size=1)
                # 不知道为什么将train写在supervised_learning里面的时候模型会不训练，因此拿出来了
                # 因为save_count会根据存储次数而增加，当save_count为0的时候意味着已经增加了save_rate个元组
                # 为了避免过拟合，因此在此时进行训练一次
                if Msl.red.save_count == 0:
                    red_sl_model.train(Msl.red.st, Msl.red.at)
                    Msl.red.save_count += 1
                pi_red = supervised_learning(camp=camp_red, sl_model=red_sl_model, st=st, actions=red_actions)
                sigma_red = (1 - eta) * pi_red + eta * beta_red
                # plot(beta_red, pi_red, sigma_red)
                # sigma dim=8100
                action = np.argmax(sigma_red)
                # action 0 ~ 8099
                available_policy = np.zeros(8100)
                available_policy = convert_action_to_array(red_actions, available_policy)
                if available_policy[action] == 0:
                    action = np.argmax(convert_action_to_array(random.sample(red_actions, 1)[0]))
                tup = (st_1, at_1, sigma_red[action] * (30 - 2 * no_eat_round) / 30, st, done)
                Mrl.update(tup=tup, camp=camp_red)
                at = convert_num_to_array(action)
                # at dim=8100
                if action == np.argmax(beta_red):
                    # if action == beta_red:
                    tup = (st, at)
                    Msl.update(tup=tup, camp=camp_red)
                decision = convert_num_to_action(action)
                print(f'red: \n'
                      f'pi max = {np.argmax(pi_red)}, {pi_red[np.argmax(pi_red)]};\n'
                      f'beta max = {np.argmax(beta_red)}, {beta_red[np.argmax(beta_red)]};\n'
                      f'sigma max = {np.argmax(sigma_red)}, {sigma_red[np.argmax(sigma_red)]};\n'
                      f'decision : {decision}\n')
                # decision string "a b c d"
            else:
                beta_black = reinforcement_learning(Mrl=Mrl, camp=camp_black, dqn_agent=black_agent, st=st, actions=black_actions, batch_size=1)
                if Msl.black.save_count == 0:
                    black_sl_model.train(Msl.black.st, Msl.black.at)
                    Msl.black.save_count += 1
                pi_black = supervised_learning(camp=camp_black, sl_model=black_sl_model, st=st, actions=black_actions)
                sigma_black = -(1 - eta) * pi_black + eta * beta_black
                # plot(beta_black, pi_black, sigma_black)
                action = np.argmin(sigma_black)
                available_policy = np.zeros(8100)
                available_policy = convert_action_to_array(black_actions, available_policy)
                if available_policy[action] == 0:
                    action = np.argmax(convert_action_to_array(random.sample(red_actions, 1)[0]))
                tup = (st_1, at_1, sigma_black[action] * (30 - 2 * no_eat_round) / 30, st, done)
                Mrl.update(tup=tup, camp=camp_black)
                at = convert_num_to_array(action)
                if action == np.argmin(beta_black):
                    tup = (st, at)
                    Msl.update(tup=tup, camp=camp_black)
                decision = convert_num_to_action(action)
                print(f'black: \n'
                      f'pi max = {np.argmax(pi_black)}, {pi_black[np.argmax(pi_black)]};\n'
                      f'beta min = {np.argmin(beta_black)}, {beta_black[np.argmin(beta_black)]};\n'
                      f'sigma min = {np.argmin(sigma_black)}, {sigma_black[np.argmin(sigma_black)]};\n'
                      f'decision : {decision}\n')
        if done == not_end and game_round == 1 and turn == camp_red:
            at = random_action(actions=red_actions)
            decision = convert_num_to_action(np.argmax(at))
        if game_round > 1:
            st_2 = st_1
            at_2 = at_1
        st_1 = st
        at_1 = at
        chess_num_prev = chess_num_now
        client.send(decision.encode("utf-8"))
        if decision == "end":
            break
        if turn == camp_red:
            turn = camp_black
        else:
            turn = camp_red
client.close()
