# test

import numpy as np

a = np.random.rand(4, 4)
b = np.random.rand(4, 4)

def matmul(a, b):
    return a.dot(b)

res = matmul(a, b)