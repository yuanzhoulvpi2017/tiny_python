from multiprocessing import Pool
from tqdm import tqdm
import time


def myf(x):
    time.sleep(1)
    return x * x


if __name__ == '__main__':
    value_x= range(20)
    P = Pool(processes=4)

    res = [P.apply_async(func=myf, args=(i, )) for i in value_x]
    result = [i.get(timeout=2) for i in res]

    print(result)