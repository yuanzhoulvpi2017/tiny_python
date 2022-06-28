import json
import pandas as pd
from pandas.api.types import is_object_dtype, is_numeric_dtype, is_datetime64_any_dtype


class BarRace(object):
    def __init__(self, pandas_df,
                 bar_color_map=None,
                 show_date_format=None):

        # process data
        self.target_columns_name = ['data_value', 'data_class', 'data_date']
        self.show_date_format = show_date_format
        self.plot_data = self.clean_data(pandas_df.copy())

        self.__pandas_data = self.plot_data
        self.detect_df_format(self.__pandas_data)
        self.detect_df_dtypes(self.__pandas_data)

        # preocess bar color
        self.bar_color_map = bar_color_map

        self.__filename = None
        self.__render_html = None
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
<script>
    var dom = document.getElementById("container");
    var myChart = echarts.init(dom);
    const updateFrequency = 2000;
    const dimension = 0;
    const model_data = {
    "raw_data":__raw_data,
    "bar_color_map":__bar_color_map,

    }


    const years = [];
    for (let i = 0; i < model_data.raw_data.length; ++i) {
        if (years.length === 0 || years[years.length - 1] !== model_data.raw_data[i][2]) {
            years.push(model_data.raw_data[i][2]);
        }
    }
    let startIndex = 0;
    let startYear = years[startIndex];
    option = {
        grid: {
            top: 10,
            bottom: 30,
            left: 200,
            right: 80
        },
        xAxis: {
            max: 'dataMax',
            axisLabel: {
                formatter: function (n) {
                    return Math.round(n) + '';
                }
            }
        },
        dataset: {
            source: model_data.raw_data.slice(1).filter(function (d) {
                return d[2] === startYear;
            })

        },
        yAxis: {
            type: 'category',
            inverse: true,
            max: 10,
            axisLabel: {
                show: true,
                fontSize: 14,
                formatter: function (value) {
                    return value;
                },
                rich: {
                    flag: {
                        fontSize: 25,
                        padding: 5
                    }
                }
            },
            animationDuration: 300,
            animationDurationUpdate: 300
        },
        series: [
            {
                realtimeSort: true,
                seriesLayoutBy: 'column',
                type: 'bar',
                itemStyle: {
                    color: function (param) {
                         return model_data.bar_color_map[param.value[1]] || '#5470c6';
                     }
                },
                encode: {
                    x: dimension,
                    y: 1
                },
                label: {
                    show: true,
                    precision: 1,
                    position: 'right',
                    valueAnimation: true,
                    fontFamily: 'monospace'
                }
            }
        ],
        // Disable init animation.
        animationDuration: 0,
        animationDurationUpdate: updateFrequency,
        animationEasing: 'linear',
        animationEasingUpdate: 'linear',
        graphic: {
            elements: [
                {
                    type: 'text',
                    right: 160,
                    bottom: 60,
                    style: {
                        text: startYear,
                        font: 'bolder 80px monospace',
                        fill: 'rgba(100, 100, 100, 0.25)'
                    },
                    z: 100
                }
            ]
        }
    };
    for (let i = startIndex; i < years.length - 1; ++i) {
        (function (i) {
            setTimeout(function () {
                updateYear(years[i + 1]);
            }, (i - startIndex) * updateFrequency);
        })(i);
    }

    function updateYear(year) {
        let source = model_data.raw_data.slice(1).filter(function (d) {
            // console.log(d.data_date);
            return d[2] === year;
        });
        option.series[0].data = source;
        option.graphic.elements[0].style.text = year;
        myChart.setOption(option);
        // }
    }

</script>
</body>
</html>
        """

    def render_html_function(self):
        # render data
        data2str = self.__pandas_data.to_json(orient='values')
        self.__render_html = self.__base_html.replace("__raw_data", data2str)

        # render bar color

        if self.bar_color_map is None:
            self.__render_html = self.__render_html.replace("__bar_color_map", "{}")
        else:
            if isinstance(self.bar_color_map, dict):
                self.__render_html = self.__render_html.replace("__bar_color_map", json.dumps(self.bar_color_map))

    def save_html(self, filename):
        self.__filename = filename
        with open(file=self.__filename, encoding='utf-8', mode='w') as f:
            f.write(self.__render_html)

    def __call__(self, *args, **kwargs):
        self.render_html_function()

    def detect_df_format(self, data):
        # target_columns_name = ['data_value', 'data_class', 'data_date']
        data_columns_list = data.columns.tolist()
        for i in self.target_columns_name:
            if i not in data_columns_list:
                raise ValueError(f"`{i}` must in data columns, but do not detect this column<`{i}`> in your data")

    def detect_df_dtypes(self, data):
        # target_columns_name = ['data_value', 'data_class', 'data_date']
        for i in self.target_columns_name:
            if i == 'data_value':
                if not is_numeric_dtype(data[i]):
                    raise ValueError(f"the data column: `{i}` must be numeric dtype")

            elif i == 'data_class':
                if not is_object_dtype(data[i]):
                    raise ValueError(f"the data column: `{i}` must be string dtype")

            elif i == 'data_date':
                if not is_datetime64_any_dtype(data[i]):
                    print(
                        f"the data column: `{i}` is not datetime dtype. but you'd better set this column type to datetime")
                if is_numeric_dtype(data[i]):
                    print(
                        f"the data column: `{i}` is numeric dtype. may be this data is datetime('year')")

    def clean_data(self, data_):
        if is_datetime64_any_dtype(data_['data_date']):
            if self.show_date_format is None:
                data_['data_date'] = data_['data_date'].dt.strftime(self.show_date_format)

        if is_numeric_dtype(data_['data_date']):
            if str(data_['data_date'].tolist()[0]) == 4:
                print(f"ignore params: `{self.show_date_format}`")

        data_ = data_.sort_values(by=['data_date'])
        data_ = data_[['data_value', 'data_class', 'data_date']]

        return data_


if __name__ == '__main__':
    # data demo
    data = pd.read_json(
        "https://fastly.jsdelivr.net/gh/apache/echarts-website@asf-site/examples/data/asset/data/life-expectancy-table.json")
    data.columns = data.iloc[0, :]
    data = data.iloc[1:, ]

    data = data[['Population', 'Country', 'Year']]
    data['Income'] = data['Population'].astype('int')
    data['Year'] = data['Year'].astype('int')
    data = data.rename(columns={'Income': 'data_value', "Country": 'data_class', 'Year': 'data_date'})

    bar_color_map = {
        'Australia': '#00008b',
        'Canada': '#f00',
        'China': '#ffde00',
        'Cuba': '#002a8f',
        'Finland': '#003580',
        'France': '#ed2939',
        'Germany': '#000',
        'Iceland': '#003897',
        'India': '#f93',
        'Japan': '#bc002d',
        'North Korea': '#024fa2',
        'South Korea': '#000',
        'New Zealand': '#00247d',
        'Norway': '#ef2b2d',
        'Poland': '#dc143c',
        'Russia': '#d52b1e',
        'Turkey': '#e30a17',
        'United Kingdom': '#00247d',
        'United States': '#b22234'
    }

    # start plot data
    br = BarRace(pandas_df=data)
    br = BarRace(pandas_df=data, bar_color_map=bar_color_map)

    br()
    br.save_html(filename="绘制racebar0625.html")
