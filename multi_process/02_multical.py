# 遇到一个大的数据，一个比较复杂的计算，使用并行，可以极大的提高计算效率

from multiprocessing import Pool
import time
from tqdm import tqdm

def myf(x):
    time.sleep(1)
    return x * x

if __name__ == '__main__':
    print('-- start run ---')
    value_x = range(20)
    P = Pool(processes=4)
    value_y = P.map(func=myf, iterable=value_x)
    print(value_y)
