import numpy as np
import matplotlib.pyplot as plt

x = np.array([0.05, 0.05, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04, 0.04, 0.03, 0.03, 0.03, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01])
y = np.array([22701, 22405, 22076, 22452, 22481, 11414, 11421, 11708, 11462, 11418, 4735, 4780, 4729, 4710, 4777, 1500, 1444, 1455, 1414, 1442, 170, 165, 191, 168, 177])

w = np.linspace(0, 0.05, num = 100)
fw = []
for i in range(len(w)):
    fw.append(178433024*w[i]**3)

plt.plot(w, fw, label='y = (1024C3) x**3')
plt.legend()
plt.scatter(x, y, alpha=0.5)
plt.xlabel('p')
plt.ylabel('# triangles')
plt.savefig('plot.png')
plt.show()
