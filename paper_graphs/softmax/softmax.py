import math
x = [3.0, 5.0, 4.0, 6.0, 3.0]
z_exp = [math.exp(i) for i in x]
sum_z_exp = sum(z_exp)
softmax = [round(i / sum_z_exp, 3) for i in z_exp]
print(softmax)