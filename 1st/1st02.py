# 爬取百度LOGO

import urllib.request

# URL地址
url = 'https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'

# 创建请求对象
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

# 读取信息
data = response.read()
# print(data)

# 将图片进行存储
with open("baidu.png", "wb") as f:
    f.write(data)