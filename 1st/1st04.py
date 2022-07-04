import requests

# 要访问的URL
url_page = "https://tool.lu/ip/"

# 代理服务器
proxy = "121.41.8.23:16818"

# 用户名和密码
username = "469041623"
password = "fv1cq0kl"

proxies = {
    'http': 'http://%(user)s:%(pwd)s@%(ip)s/' % {'user': username, 'pwd': password, 'ip': proxy},
    'https': 'http://%(user)s:%(pwd)s@%(ip)s/' % {'user': username, 'pwd': password, 'ip': proxy}
}

# 使用请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/102.0.0.0 Safari/537.36"}

req = requests.get(url=url_page, proxies=proxies, headers=headers)
if req.status_code == 200:
    print(req.content.decode("utf8"))