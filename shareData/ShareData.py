from multiprocessing import shared_memory
import pandas as pd
import os
import yaml
import shutil

class ShareDataFrame(object):
    def __init__(self):
        self.columnsname_shm = None
        self.value_shm_list = []
        self.yaml_file_name = 'temp/dfdatainfo.yaml'
        self.shm_and_colname = None
        self.read_columnname = None
        self.read_shm_data = None
        self.readdf = None
        self.writer_shm = []

    def init_env(self):
        if os.path.exists("temp"):
            # os.remove("temp")
            # os.rmdir("temp")
            shutil.rmtree("temp")
            os.mkdir("temp")
        else:
            os.mkdir("temp")

    def df2memory(self, data):
        self.init_env()
        self.columnsname_shm = data.columns.tolist()
        for index, tempcolname in enumerate(self.columnsname_shm):
            tempdata = shared_memory.ShareableList(sequence=data[tempcolname].tolist())
            self.writer_shm.append(tempdata)
            self.value_shm_list.append([self.columnsname_shm[index], tempdata.shm.name])
            print(f"clumnname: {tempcolname}, shm_name: {tempdata.shm.name}")

        # save data
        with open(file=self.yaml_file_name, mode='w', encoding='utf-8') as f:
            f.write(yaml.dump(self.value_shm_list))

    def memory2df(self):
        # open data
        with open(file=self.yaml_file_name, mode='r', encoding='utf-8') as f:
            read_yaml = yaml.load(stream=f.read(), Loader=yaml.FullLoader)
        self.shm_and_colname = read_yaml
        self.read_columnname = [i[0] for i in self.shm_and_colname]
        self.read_shm_data = [shared_memory.ShareableList(name=i[1]) for i in self.shm_and_colname]
        self.readdf = pd.DataFrame({
            self.read_columnname[index]: list(self.read_shm_data[index])
            for index, tempcolname in enumerate(self.read_shm_data)
        })
        self.readdf.columns = self.read_columnname
        print(read_yaml)

        return self.readdf

    def close_write(self):
        for shm_temp in self.writer_shm:
            shm_temp.shm.close()

    def close_read(self):
        for shm_temp in self.read_shm_data:
            shm_temp.shm.close()
            shm_temp.shm.unlink()
