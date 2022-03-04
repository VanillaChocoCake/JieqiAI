# 监督学习与分类
import os

from tensorflow.keras import optimizers
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D, Dense, MaxPooling2D
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import add, BatchNormalization, Flatten
from tensorflow.keras.models import load_model, Model

from AI_Functions import *
from localtime import localtime


def create_model(learning_rate):
    def residual_module(layer_in, n_filters):
        merge_input = layer_in
        if layer_in.shape[-1] != n_filters:
            merge_input = Conv2D(n_filters, (1, 1), padding='same', activation='relu')(layer_in)
        conv1 = Conv2D(n_filters, (1, 1), padding='same', activation='relu')(layer_in)
        batch_norm = BatchNormalization()(conv1)
        layer_out = add([batch_norm, merge_input])
        layer_out = Activation('relu')(layer_out)
        return layer_out

    visible = Input(shape=(10, 9, 16))
    x = residual_module(visible, 1024)
    maxpooling_x = MaxPooling2D()(x)
    y = residual_module(maxpooling_x, 512)
    maxpooling_y = MaxPooling2D()(y)
    z = Dense(1024, activation="relu")(maxpooling_y)
    flatten = Flatten()(z)
    final = Dense(512, activation="relu")(flatten)
    action = Dense(8100, activation="softmax")(final)
    model = Model(inputs=visible, outputs=action)
    sgd = optimizers.SGD(learning_rate=learning_rate)
    model.compile(optimizer=sgd, loss='binary_crossentropy')
    return model


class SLModel:
    def __init__(self, camp, learning_rate=0.005):
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

    def train(self, st, at, epochs=10):
        self.model.fit(st, at, epochs=epochs)
        self.save_count += 1
        if self.save_count > self.save_rate:
            self.save()
            self.save_count = 0

    def generate_figure(self):
        from tensorflow.keras.utils import plot_model
        plot_model(self.model, to_file=f'model_{localtime()}.png')

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
    """
    if camp == camp_red and len(Msl.red.st) > 0:
        sl_model.train(Msl.red.st, Msl.red.at, camp)
    elif camp == camp_black and len(Msl.black.st) > 0:
        sl_model.train(Msl.black.st, Msl.black.at, camp)
    # 删除掉这一步的原因在于，函数运行到这里后，并不会训练模型
    # 不要问我为什么，我也不知道
    """
    st = np.array([st])
    average_policy = sl_model.predict(st)
    available_policy = np.zeros(8100)
    available_policy = convert_action_to_array(actions, available_policy)
    average_policy = generate_policy(average_policy, available_policy)
    # src, dst = convert_num_to_action(average_policy)
    if camp == camp_red:
        return average_policy
    else:
        return -average_policy
