import os

from tensorflow.keras import optimizers
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model

from ai.AI_Functions import *
from localtime import localtime


def create_model(learning_rate=0.1):
    model = Sequential()
    # 这个输入不好，建议参考AlphaZero论文中的输入
    model.add(Input(shape=(10, 9, 16)))
    model.add(Conv2D(512, 1))
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(MaxPooling2D())
    model.add(Activation("relu"))
    model.add(Flatten())
    model.add(Dense(8100, activation="tanh"))
    sgd = optimizers.SGD(learning_rate=learning_rate)
    model.compile(optimizer=sgd, loss='mean_squared_error')
    model.summary()
    return model


class DQN:
    def __init__(self, camp=camp_red, learning_rate=0.1):
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
        self.epsilon = 0.1
        self.epsilon_min = 0.0001
        self.epsilon_decay = 0.99
        self.update_rate = 100
        self.update_count = 0
        self.save_count = 0
        self.save_rate = 200
        self.target_model = create_model(learning_rate=self.learning_rate)
        self.target_model.set_weights(self.model.get_weights())
        # self.model.summary()

    def train(self, Mrl, batch_size=128):
        if batch_size == 0:
            return None
        if self.camp == camp_red:
            mini_batch = random.sample(Mrl.red.rlmemory, batch_size)
        else:
            mini_batch = random.sample(Mrl.black.rlmemory, batch_size)
        for st_prev, at_prev, rt, st, ct in mini_batch:
            st_prev = np.array([st_prev])
            np.reshape(at_prev, 8100)
            st = np.array([st])
            if self.camp == camp_red:
                if ct != end:
                    target = rt + self.gamma * np.max(self.target_model.predict(st))
                else:
                    target = rt
            else:
                if ct != end:
                    target = rt + self.gamma * np.min(self.target_model.predict(st))
                else:
                    target = rt
            target_prediction = self.model.predict(st_prev)
            target_prediction[0][np.argmax(at_prev)] = target
            self.model.fit(np.reshape(st_prev, (1, 10, 9, 16)),
                           np.reshape(target_prediction, (1, 8100)),
                           epochs=2,
                           verbose=0)
        self.update_count += 1
        self.save_count += 1
        if self.update_count > self.update_rate:
            self.update_target_model()
            self.update_count = 0
        if self.save_count > self.save_rate:
            self.save()
            self.save_count = 0

    def predict(self, st):
        action = self.model.predict(st)[0]
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        else:
            self.epsilon = self.epsilon_min
        return action

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def generate_figure(self):
        from tensorflow.keras.utils import plot_model
        plot_model(self.model, to_file=f'rl_model_pic.png')

    def save(self):
        if self.camp == camp_red:
            try:
                os.rename("rl_model_red.h5", f'rl_model_red_{localtime()}.h5')
            except:
                pass
            self.model.save("rl_model_red.h5")
        else:
            try:
                os.rename("rl_model_black.h5", f'rl_model_black_{localtime()}.h5')
            except:
                pass
            self.model.save("rl_model_black.h5")


def reinforcement_learning(Mrl, camp, dqn_agent, st, actions, batch_size=128):
    """
    return: dim=8100
    """
    if camp == camp_red and len(Mrl.red.rlmemory) > batch_size and Mrl.red.save_count == 0:
        print("强化学习中...")
        dqn_agent.train(Mrl, batch_size=batch_size)
    elif camp == camp_black and len(Mrl.black.rlmemory) > batch_size and Mrl.black.save_count == 0:
        print("强化学习中...")
        dqn_agent.train(Mrl, batch_size=batch_size)
    random_policy = random_action(actions=actions)
    st = np.array([st])
    best_policy = dqn_agent.predict(st)
    available_policy = np.zeros(8100)
    available_policy = convert_action_to_array(actions, available_policy)
    beta = generate_policy(best_policy, available_policy)
    num = random.uniform(0, 1)
    if num > dqn_agent.epsilon:
        return beta
    else:
        if camp == camp_red:
            return random_policy
        else:
            return -random_policy

def rl(camp, dqn_agent, st, actions):
    """
    return: dim=8100
    """
    random_policy = random_action(actions=actions)
    st = np.array([st])
    best_policy = dqn_agent.predict(st)
    available_policy = np.zeros(8100)
    available_policy = convert_action_to_array(actions, available_policy)
    beta = generate_policy(best_policy, available_policy)
    num = random.uniform(0, 1)
    if num > dqn_agent.epsilon:
        return beta
    else:
        if camp == camp_red:
            return random_policy
        else:
            return -random_policy