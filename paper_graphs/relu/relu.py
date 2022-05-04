import numpy as np
from matplotlib import pyplot as plt


def relu(x):
    return np.where(x < 0, 0, x)


def relu_dx(x):
    return np.where(x < 0, 0, 1)


x = np.arange(-5, 5, 0.01)
fx = relu(x)
fx_dx = relu_dx(x)
plt.plot(x, fx)
plt.savefig("relu/relu.png")
plt.close()
plt.plot(x, fx_dx)
plt.savefig("relu/relu_dx.png")