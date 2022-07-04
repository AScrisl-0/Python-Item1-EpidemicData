# 爬取百度首页

import urllib.request

# URL地址
url = 'http://www.baidu.com/'

# 发送请求
request = urllib.request.Request(url)
# print(request
# 响应信息
response = urllib.request.urlopen(request)
# 读取数据
data = response.read()
# print(data)
# 将byte类型转为str类型
html = data.decode("utf8")

with open("baidu.html","w",encoding="utf8") as f:
    f.write(html)
