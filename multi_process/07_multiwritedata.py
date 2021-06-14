# multi sub process write data to one data (python dict)
# use Pool

from multiprocessing import Pool, Manager
import os
import time
import pandas as pd
from tqdm import tqdm


def worker(id, save_data):
    time.sleep(1)
    save_data[id] = {
        '子进程': [os.getpid()],
        '父进程': [os.getppid()],
        '进程id': [id]
    }


if __name__ == "__main__":
    finaldata = Manager().dict()

    P = Pool(processes=20)

    # reslist = []
    # for i in tqdm(range(200)):
    #     res = P.apply_async(func=worker, args=(i, finaldata))
    #     reslist.append(res)

    reslist = [P.apply_async(func=worker, args=(i, finaldata)) for i in range(200)]

    [res.get(timeout=200) for res in tqdm(reslist)]

    finaldata = pd.concat([pd.DataFrame(value) for (key, value) in finaldata.items()])

    print(finaldata)
