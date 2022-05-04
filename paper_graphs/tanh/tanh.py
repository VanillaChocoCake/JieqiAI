import numpy as np
from matplotlib import pyplot as plt


def tanh(x):
    return np.tanh(x)


x = np.arange(-5, 5, 0.01)
fx = tanh(x)
plt.plot(x, fx)
plt.savefig("tanh.png")
