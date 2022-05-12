# 展示代码，AI输入
import socket
from SL import *
import numpy as np
from AI_Functions import *
from RL import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
red_sl_model = SLModel(camp=camp_red)
black_sl_model = SLModel(camp=camp_black)
red_agent = DQN(camp=camp_red)
black_agent = DQN(camp=camp_black)
while True:
    side = int(input("AI:红方1，黑方0："))
    while True:
        board_info = client.recv(2048)
        message = board_info.decode("utf-8")
        message = message.split(" ")
        board = translate_message(message)
        st = convert_board_to_array(board)
        red_actions, black_actions = available_actions(board)
        if side == camp_red:
            pi = supervised_learning(camp=camp_red, sl_model=red_sl_model, st=st, actions=red_actions)
            beta = rl(camp=camp_red, dqn_agent=red_agent, st=st, actions=red_actions)
            normalized_beta = normalize_policy(beta)
            sigma = (1 - eta) * pi + eta * normalized_beta
            action = np.argmax(sigma)
            available_policy = np.zeros(8100)
            available_policy = convert_action_to_array(red_actions, available_policy)
            if available_policy[action] < 1:
                action = np.argmax(convert_action_to_array(random.sample(red_actions, 1)[0]))
        else:
            pi = supervised_learning(camp=camp_black, sl_model=black_sl_model, st=st, actions=black_actions)
            beta = rl(camp=camp_black, dqn_agent=black_agent, st=st, actions=black_actions)
            normalized_beta = normalize_policy(beta)
            sigma = -(1 - eta) * pi + eta * normalized_beta
            action = np.argmin(sigma)
            available_policy = np.zeros(8100)
            available_policy = convert_action_to_array(black_actions, available_policy)
            if available_policy[action] < 1:
                action = np.argmax(convert_action_to_array(random.sample(black_actions, 1)[0]))
        decision = convert_num_to_action(action)
        client.send(decision.encode("utf-8"))


