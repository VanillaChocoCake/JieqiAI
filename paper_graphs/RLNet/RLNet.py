from ai.RL import *
from tensorflow.keras.utils import plot_model
net = DQN()
plot_model(net.model, to_file="rl.png", show_shapes=True, dpi=120)
