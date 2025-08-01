import requests
from lxml import etree
import os
# 请求url
url = 'https://www.joyread.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
# 发送请求
resp = requests.get(url, headers=headers)
# 设置编码
resp.encoding = 'utf-8'
e = etree.HTML(resp.text)
print(resp.text)