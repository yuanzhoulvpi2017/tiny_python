# 在不使用numpy的时候，进行简单的并行计算

import time
from tqdm import tqdm

def myf(x):
    time.sleep(1)
    return x * x

if __name__ == '__main__':
    listx = range(10)
    listy = []

    for i in tqdm(listx):
        temp_value = myf(x=i)
        listy.append(temp_value)
    print('final y:')
    print(listy)
