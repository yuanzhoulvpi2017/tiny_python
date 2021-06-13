from multiprocessing import Pool, TimeoutError
import time
from tqdm import tqdm


def myf(x):
    # print('in worker')
    if x % 5 == 0:
        time.sleep(20.2)
    else:
        time.sleep(0.3)
    return x * x


def safely_get(value, timeout=2):
    # print('in safelt get')
    try:
        value = value.get(timeout=timeout)
    except TimeoutError:
        value = 0
    return value


if __name__ == '__main__':
    P = Pool(processes=10)
    value = range(40)
    pbar = tqdm(total=len(value))

    res_temp = [P.apply_async(func=myf, args=(i,), callback=lambda _: pbar.update(1)) for i in value]
    # result = [res.get(timeout=3) for res in res_temp]
    result = [safely_get(res, timeout=1) for res in res_temp]

    print(result)
