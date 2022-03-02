# 监督学习与分类
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras import optimizers
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


def create_model():
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
    action = Dense(8100, activation="tanh")(final)
    model = Model(visible, action)
    sgd = optimizers.SGD(learning_rate=0.005)
    model.compile(optimizer=sgd, loss='binary_crossentropy')
    return model


class SLModel:
    def __init__(self, model=None):
        if model is None:
            self.model = create_model()
        else:
            self.model = model

    def predict(self, st):
        action = self.model.predict(st)[0]
        """
        while np.min(abs(action)) < 0.01:
            action = action * 100
        """
        return action

    def train(self, st, at, camp, epochs=300):
        self.model.fit(st, at, epochs=epochs)
        if camp == camp_red:
            try:
                os.rename("sl_model_red.h5", "sl_model_red " + localtime() + ".h5")
            except:
                pass
            self.model.save("sl_model_red.h5")
        else:
            try:
                os.rename("sl_model_black.h5", "sl_model_black " + localtime() + ".h5")
            except:
                pass
            self.model.save("sl_model_black.h5")

    def generate_figure(self):
        from tensorflow.keras.utils import plot_model
        plot_model(self.model, to_file="model " + localtime() + ".png")


def supervised_learning(Msl, camp, sl_model, st, actions):
    """
    监督学习
    :param sl_model: 监督学习模型
    :param Msl: 监督学习用的蓄水池采样缓存(st,at)
    :return: 平均策略Fs
    :param camp: 阵营
    :param st: 状态
    :param actions: 所有合法行动
    需要随机梯度下降法
    """
    if camp == camp_red:
        sl_model.train(Msl.red.st, Msl.red.at, camp)
    else:
        sl_model.train(Msl.black.st, Msl.black.at, camp)
    average_policy = sl_model.predict(st)
    available_policy = np.zeros(8100)
    available_policy = convert_action_to_array(actions, available_policy)
    average_policy = select_policy(average_policy, available_policy, camp)
    src, dst = convert_num_to_action(average_policy)
    return src, dst
