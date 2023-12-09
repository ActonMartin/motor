import numpy as np

list = [1,2,3,4,5,6,7,8,9]
a = np.array(list).reshape(3,3)
print(a)
b = a[:1,:1:-1]
print(b)

