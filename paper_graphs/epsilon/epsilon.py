import numpy as np
import matplotlib.pyplot as plt


def epsilon(x):
    res = []
    for i in range(0, len(x)):
        tmp = 0.7 * np.power(0.99, i)
        if tmp > 0.1:
            res.append(tmp)
        else:
            res.append(0.1)
    return res


x = np.arange(0, 400, 1)
y = epsilon(x)
plt.plot(x, y)
plt.xlabel("round")
plt.ylabel("epsilon")
plt.savefig("epsilon.png")
