# user-agent使用

import urllib.request

url="https://dig.chouti.com/"


headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}

# 发送请求
request = urllib.request.Request(url,headers=headers)
# print(request
# 响应信息
response = urllib.request.urlopen(request)
# 读取数据
data = response.read()
# print(data)
# 将byte类型转为str类型
html = data.decode("utf8")

with open("chouti.html","w",encoding="utf8") as f:
    f.write(html)