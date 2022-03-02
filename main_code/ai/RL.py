import copy
import random

import numpy as np
from tensorflow.keras import optimizers
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D, Dense, MaxPooling2D, MaxPooling3D
from tensorflow.keras.layers import add, BatchNormalization, Flatten
from tensorflow.keras.losses import BinaryCrossentropy, MeanSquaredError
import tensorflow as tf
import tensorflow.keras as keras
from localtime import localtime
import os
from const import *
from AI_Functions import *


def create_model(learning_rate=0.1):
    model = Sequential()
    model.add(Input(shape=(10, 9, 16)))
    model.add(Conv2D(1024, 1, activation="relu"))
    model.add(MaxPooling2D())
    model.add(Conv2D(512, 1, activation="relu"))
    model.add(Dense(1024, activation="relu"))
    model.add(Flatten())
    model.add(Dense(512, activation="relu"))
    model.add(Dense(8100, activation="tanh"))
    sgd = optimizers.SGD(learning_rate=learning_rate)
    model.compile(optimizer=sgd, loss='binary_crossentropy')
    return model


class DQN:
    def __init__(self, camp, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.camp = camp
        try:
            if self.camp == camp_red:
                self.model = load_model("rl_model_red.h5")
            else:
                self.model = load_model("rl_model_black.h5")
        except:
            self.model = create_model(self.learning_rate)
        self.gamma = 1.0
        self.epsilon = 0.2
        self.epsilon_min = 1e-6
        self.epsilon_decay = 0.995
        self.update_rate = 100
        self.update_count = 0
        self.target_model = copy.deepcopy(self.model)
        # self.model.summary()

    def train(self, Mrl, batch_size=128):
        if self.camp == camp_red:
            mini_batch = random.sample(Mrl.red.rlmemory, batch_size)
        else:
            mini_batch = random.sample(Mrl.black.rlmemory, batch_size)
        for st_prev, at_prev, rt, st, ct in mini_batch:
            st_prev = np.array([st_prev])
            np.reshape(at_prev, 8100)
            st = np.array([st])
            if ct != 0:
                target = rt + self.gamma * np.max(self.target_model.predict(st))
            else:
                target = rt
            target_prediction = self.model.predict(st_prev)
            target_prediction[0][np.argmax(at_prev)] = target
            self.model.fit(np.reshape(st_prev, (1, 10, 9, 16)), np.reshape(target_prediction, (1, 8100)), epochs=1,
                           verbose=0)
        self.save()
        self.update_count += 1
        if self.update_count > self.update_rate:
            self.update_target_model()
            self.update_count = 0

    def predict(self, st):
        action = self.model.predict(st)[0]
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        return action

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def save(self):
        if self.camp == camp_red:
            try:
                os.rename("rl_model_red.h5", "rl_model_red " + localtime() + ".h5")
            except:
                pass
            self.model.save("rl_model_red.h5")
        else:
            try:
                os.rename("rl_model_black.h5", "rl_model_black " + localtime() + ".h5")
            except:
                pass
            self.model.save("rl_model_black.h5")


def reinforcement_learning(Mrl, camp, dqn_agent, st, actions, batch_size=128):
    if camp == camp_red:
        if len(Mrl.red.rlmemory) > batch_size:
            dqn_agent.train(Mrl)
    else:
        if len(Mrl.black.rlmemory) > batch_size:
            dqn_agent.train(Mrl)
    best_policy = dqn_agent.predict(st)
    available_policy = np.zeros(8100)
    available_policy = convert_action_to_array(actions, available_policy)
    best_policy = select_policy(best_policy, available_policy, camp)
    random_policy = random.sample(actions, 1)
    random_policy = convert_action_to_array(random_policy)
    num = random.uniform(0, 1)
    if num < dqn_agent.epsilon:
        return best_policy
    else:
        return random_policy


