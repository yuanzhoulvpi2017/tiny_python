import numpy as np
import pandas as pd
import requests
import json


class SanKey(object):
    """
    使用echarts做sankey
    """

    def __init__(self, pandasdf, title):
        """

        :param pandasdf: 要求是pandas的DataFrame，必须含有source,target,value三列
        :param title: 标题
        """
        self.__df = pandasdf
        self.__sankey_title = title
        self.__base_html = """
<!--
    THIS EXAMPLE WAS DOWNLOADED FROM https://echarts.apache.org/examples/zh/editor.html?c=sankey-energy
-->
<!DOCTYPE html>
<html style="height: 100%">
<head>
    <meta charset="utf-8">
</head>
<body style="height: 100%; margin: 0">
<div id="container" style="height: 100%"></div>

<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<!-- Uncomment this line if you want to dataTool extension
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts@5/dist/extension/dataTool.min.js"></script>
-->
<!-- Uncomment this line if you want to use gl extension
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts-gl@2/dist/echarts-gl.min.js"></script>
-->
<!-- Uncomment this line if you want to echarts-stat extension
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts-stat@latest/dist/ecStat.min.js"></script>
-->
<!-- Uncomment this line if you want to use map
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts@5/map/js/china.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts@5/map/js/world.js"></script>
-->
<!-- Uncomment these two lines if you want to use bmap extension
<script type="text/javascript" src="https://api.map.baidu.com/api?v=2.0&ak=<Your Key Here>"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts@5/dist/extension/bmap.min.js"></script>
-->
<script type="text/javascript">
    var dom = document.getElementById("container");
    var myChart = echarts.init(dom);
    var app = {};
    myChart.showLoading();
    var data = {
        "nodes": node_in_html,
        "links": link_in_html,
        "title": 'title_in_html'
    }
    var option = {
        title: {
            text: data.title
        },
        tooltip: {
            trigger: 'item',
            triggerOn: 'mousemove'
        },
        series: [
            {
                type: 'sankey',
                data: data.nodes,
                links: data.links,
                emphasis: {
                    focus: 'adjacency'
                },
                lineStyle: {
                    color: 'gradient',
                    curveness: 0.5
                }
            }
        ]
    };
    myChart.hideLoading();
    myChart.setOption(option);
    if (option && typeof option === 'object') {
        myChart.setOption(option);
    }
</script>
</body>
</html>

"""

        self.__node_list = None
        self.__links_in_html = None
        self.__render_html = self.__base_html

    def trans_node_link(self):
        node_list = list(set(self.__df['source'].tolist() + self.__df['target'].tolist()))
        self.__node_list = json.dumps([{"name": i} for i in node_list])
        self.__links_in_html = self.__df.to_json(orient='records')

    def render_html_function(self):
        self.__render_html = self.__render_html.replace("node_in_html", self.__node_list)
        self.__render_html = self.__render_html.replace("link_in_html", self.__links_in_html)
        self.__render_html = self.__render_html.replace("title_in_html", self.__sankey_title)

    def save_html(self, filename):
        """

        :param filename: 保存文件的文件名，必须以.html结尾
        :return:
        """
        self.__filename = filename
        with open(file=self.__filename, encoding='utf-8', mode='w') as f:
            f.write(self.__render_html)

    def __call__(self, *args, **kwargs):
        self.trans_node_link()
        self.render_html_function()


def main():
    # get data
    ROOT_PATH = "https://cdn.jsdelivr.net/gh/apache/echarts-website@asf-site/examples"
    energy = ROOT_PATH + "/data/asset/data/energy.json"

    data1 = requests.get(url=energy).json()['links']
    pddata = pd.concat([pd.DataFrame({key: [item] for key, item in data.items()}) for data in data1])

    sankey_plot = SanKey(pandasdf=pddata, title="公众号: pypi")
    sankey_plot()
    sankey_plot.save_html(filename="test_sankey_0731002.html")


if __name__ == '__main__':
    main()
