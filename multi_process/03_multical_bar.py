# 相对于02，这个可以有个变动的进度条，进度条不断的衍生，但是缺点也很明显，缺少进度完成情况。
from multiprocessing import Pool
import time
from tqdm import tqdm


def myf(x):
    time.sleep(1)
    return x * x


if __name__ == '__main__':
    # print('-- start run ---')
    value_x = range(20)
    P = Pool(processes=4)
    value_y = list(tqdm(P.imap_unordered(func=myf, iterable=value_x)))
    print(value_y)
