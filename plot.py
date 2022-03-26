import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility


N = 50
x = [0.05, 0.05, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04, 0.04]
y = [22701, 22405, 22076, 22452, 22481, 11414, 11421, 11708, 11462, 11418]

plt.scatter(x, y, alpha=0.5)
plt.xlabel('p')
plt.ylabel('# triangles')
plt.show()