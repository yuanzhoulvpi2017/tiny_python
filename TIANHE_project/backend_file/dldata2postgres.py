import pandas as pd
import requests
import time
from sqlalchemy import create_engine


def line2data(line):
    line_data = pd.Series(data=[float(i) for i in line.split("|") if i != ""],
                          index=['latitude', 'longitude', 'none0', 'none1', 'none2', 'none3', 'altitude', 'none5',
                                 'norad_id', 'time', 'none8'])
    line_data['time_format'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(line_data['time']))
    return line_data


def get_satellites_location(norad_id=48274):
    try:
        url = f"https://www.n2yo.com/sat/instant-tracking.php?s={norad_id}&hlat=0&hlng=0&d=300&r=0&tz=GMT+08:00&O=n2yocom&callback="
        request_data = requests.get(url=url)
        if request_data.status_code == 200:
            finaldata = pd.DataFrame(request_data.json()[0]['pos'])['d'].apply(lambda x: line2data(x))
            finaldata['status'] = 200
        else:
            finaldata = pd.DataFrame({'status': [404]})
    except Exception as e:
        print('faild')
        finaldata = pd.DataFrame({'status': [404]})

    return finaldata


if __name__ == '__main__':

    engine = create_engine('postgresql://localhost/huzheng')

    while True:
        print(time.ctime(), '\n')
        temp_data = get_satellites_location()
        if temp_data['status'].unique().tolist()[0] == 200:
            temp_data.to_sql(con=engine, name="css_location", if_exists="replace", index=False)
            time.sleep(100)
        else:
            time.sleep(3)
