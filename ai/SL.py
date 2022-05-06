# 监督学习与分类
import os
from tensorflow.keras import optimizers
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from ai.AI_Functions import *
from localtime import localtime


def create_model(learning_rate):
    model = Sequential()
    model.add(Input(shape=(10, 9, 16)))
    model.add(Conv2D(512, 1))
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(MaxPooling2D())
    model.add(Activation("relu"))
    model.add(Flatten())
    model.add(Dense(8100, activation="softmax"))
    sgd = optimizers.SGD(learning_rate=learning_rate)
    model.compile(optimizer=sgd, loss='binary_crossentropy')
    model.summary()
    return model


class SLModel:
    def __init__(self, camp=camp_red, learning_rate=0.005):
        self.learning_rate = learning_rate
        self.camp = camp
        self.save_count = 0
        self.save_rate = 100
        try:
            if self.camp == camp_red:
                self.model = load_model("sl_model_red.h5")
            else:
                self.model = load_model("sl_model_black.h5")
        except:
            self.model = create_model(self.learning_rate)

    def predict(self, st):
        action = self.model.predict(st)[0]
        return action

    def train(self, st, at, epochs=1):
        if len(st) == 0:
            return None
        self.model.fit(st, at, epochs=epochs, verbose=0)
        self.save()

    def generate_figure(self):
        from tensorflow.keras.utils import plot_model
        plot_model(self.model, to_file=f'sl_model_pic.png')

    def save(self):
        if self.camp == camp_red:
            try:
                os.rename("sl_model_red.h5", f'sl_model_red_{localtime()}.h5')
            except:
                pass
            self.model.save("sl_model_red.h5")
        else:
            try:
                os.rename("sl_model_black.h5", f'sl_model_black_{localtime()}.h5')
            except:
                pass
            self.model.save("sl_model_black.h5")


def supervised_learning(camp, sl_model, st, actions):
    """
    监督学习
    :param sl_model: 监督学习模型
    :param camp: 阵营
    :param st: 状态
    :param actions: 所有合法行动
    :return: 平均策略Fs dim=8100
    需要随机梯度下降法
    """
    st = np.array([st])
    average_policy = sl_model.predict(st)
    available_policy = np.zeros(8100)
    available_policy = convert_action_to_array(actions, available_policy)
    average_policy = generate_policy(average_policy, available_policy)
    average_policy = normalize_policy(average_policy)
    return average_policy
