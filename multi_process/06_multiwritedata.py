# multi sub process write data to one data (python dict)

from multiprocessing import Process, Manager
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
    
    subprocess_list = []

    for i in tqdm(range(200)):
        p = Process(target=worker, args=(i, finaldata))
        subprocess_list.append(p)
        p.start()


    [p.join() for p in tqdm(subprocess_list)]

    finaldata = pd.concat([pd.DataFrame(value) for (key, value) in finaldata.items()])

    print(finaldata)
    
