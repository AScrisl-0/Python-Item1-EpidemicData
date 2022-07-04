import requests
import time

# 腾讯舆情页面是一个利用AJAX方式传输数据的。
# 需要用到的API：
# https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=localCityNCOVDataList,diseaseh5Shelf
# 这个API包含了国内当天全部的数据（确诊、死亡、治愈）
# https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayListNew,chinaDayAddListNew&limit=30
# chinaDayListNew：历史的新增疫情数据
# chinaDayAddListNew：历史的累计的疫情数据
# limit=30参数表示可以查看历史多少天的数据
# https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?adCode=440300&limit=30
# 表示的省份的历史数据，通过修改adCode=440300可以获取对应省份或者城市，limit=30可以修改获取历史天数。
# 港澳台的数据只有当天数据，没有历史数据。

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko)"
                         " Chrome/102.0.0.0 Safari/537.36",
           "Host": "api.inews.qq.com",
           "Origin": "https://news.qq.com/"
           }

def get_tencent_data():
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=localCityNCOVDataList,diseaseh5Shelf'
    response = requests.post(url, headers=headers)
    data_all = response.json()['data']  # 获取JSON数据
    data_h5 = data_all['diseaseh5Shelf']  # h5的数据
    # 当日本土数据
    data_DailyReport = data_all['localCityNCOVDataList']
    print(data_DailyReport)

if __name__ == '__main__':
    get_tencent_data()
