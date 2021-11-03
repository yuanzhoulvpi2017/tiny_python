# %%
import requests
from lxml import etree
import os
import shutil
from tqdm import tqdm
import time
import random


class BqbSeries(object):
    def __init__(self, url, project_name):
        self.big_url = url
        self.project_name = project_name

    @staticmethod
    def orderlist(url):
        """
        提取首页排行榜的所有列表
        然后将列表里面的所有内容都下载下来
        """
        web = requests.get(url)
        dom = etree.HTML(web.text)
        list_url = dom.xpath('//*[@id="bqblist"]/a[@class="bqba"]/@href')
        list_url = [f"https://fabiaoqing.com{i}" for i in list_url]

        list_name = dom.xpath('//*[@id="bqblist"]/a[@class="bqba"]/@title')
        list_name = [BqbSeries.cleanname(x) for x in list_name]

        return list_url, list_name

    @staticmethod
    def cleanname(x):
        x = x.replace("/", "").replace("\\", '')
        return x

    def url2multi(self, url):
        """
        提取一个系列页面里面的所有表情包url
        """
        web = requests.get(url)
        dom = etree.HTML(web.text)

        list_data = dom.xpath('//*[@id="bqb"]/div[1]/div[1]/div/div/div/a/@href')
        list_data = [f"https://www.fabiaoqing.com{i}" for i in list_data]
        return list_data

    def html2url(self, url):
        """
        提取一个网页里面，最主要的那个url
        """
        web = requests.get(url=url)
        temp_path = etree.HTML(web.text).xpath('//*[@id="bqb"]/div[1]/div[1]/div/div/div/img/@src')[0]
        # //*[@id="bqb"]/div[1]/div[1]/div/div/div/img
        return temp_path

    def savefile(self, url, filename, dirname):
        """
        将url里面的文件保存到文件夹中
        """
        filename_format = url.split(".")[-1]
        filename = f"{filename}.{filename_format}"

        data = requests.get(url=url)

        if dirname is None:
            save_path = filename
        else:
            save_path = os.path.join(dirname, filename)

        with open(file=save_path, mode='wb') as f:
            f.write(data.content)

    @staticmethod
    def detect_dir(dirname):
        """
        检验文件夹是否存在
        """
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
            os.mkdir(dirname)
        else:
            os.mkdir(dirname)

    def run(self):
        """
        运行部分
        """

        BqbSeries.detect_dir(dirname=self.project_name)

        """
        1. 爬链接
        """
        url_list = self.url2multi(url=self.big_url)
        for index in tqdm(range(len(url_list)), desc=f'{self.project_name}...'):
            temp_path = self.html2url(url=url_list[index])
            self.savefile(url=temp_path, filename=index, dirname=self.project_name)
            time.sleep(random.randint(0, 4))

        print('done ~')

        return 'success'


class BqbMonster(object):
    """
    怪兽模式
    批量下载热门排行榜里面的所有表情包系列
    """

    def __init__(self):
        pass

    def hot(self):
        """
        下载热门榜的前10页面
        """
        for page_index in tqdm(range(10), desc="下载排行榜..."):
            base_url = f"https://fabiaoqing.com/bqb/lists/type/hot/page/{page_index}.html"
            column_url, column_name = BqbSeries.orderlist(base_url)
            for column_page in tqdm(range(len(column_url)), desc=f"downloading :{page_index}"):
                bqb = BqbSeries(url=column_url[column_page], project_name=column_name[column_page])
                bqb.run()


if __name__ == '__main__':
    bqbmonster = BqbMonster()
    bqbmonster.hot()
