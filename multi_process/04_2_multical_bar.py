from multiprocessing import Pool
from tqdm import tqdm
import time


def myf(x):
    time.sleep(1)
    return x * x


if __name__ == '__main__':
    value_x= range(200)
    P = Pool(processes=20)

    pbar = tqdm(total=len(value_x))

    # 这里计算很快
    res = [P.apply_async(func=myf, args=(i, ), callback= lambda _: pbar.update(1)) for i in value_x]

    # 主要是看这里
    result = [i.get(timeout=2) for i in res]

    print(result)