

import numpy as np

a = np.random.rand(4, 4)
b = np.random.rand(4, 4)

def matmul(a, b):
    return a.dot(b)

if __name__ == "__main__":
    print(matmul(a, b))