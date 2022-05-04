from ai.SL import *
from tensorflow.keras.utils import plot_model
net = SLModel()
plot_model(net.model, to_file="sl.png", show_shapes=True, dpi=120)
