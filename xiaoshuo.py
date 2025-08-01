# 发送请求

# pip install requests,lxml
import requests
from lxml import etree
import os



# 请求url
url = 'https://dl.131437.xyz/book/douluodalu1/1.html'

while True:

    # 伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 发送请求
    resp = requests.get(url, headers=headers)

    # 设置编码
    resp.encoding = 'utf-8'
    # 打印响应内容


    e= etree.HTML(resp.text)
    print(e)
    info = e.xpath('//div[@class="m-post"]/p/text()')
    title = e.xpath('string(//h1)')
    url_path = e.xpath('//tr/td[2]/a/@href')[0]
    url = f"https://dl.131437.xyz{url_path}"

    # print(info)
    # print(title)
    # 保存到文件 
    os.makedirs('douluodalu', exist_ok=True)  # 确保目录存在
    with open(f'douluodalu/{title}.txt','w', encoding='utf-8') as f:
        f.write(title + '\n')
        for i in info:
            f.write(i + '\n')
    
    print(url_path)
    if url_path == '/book/douluodalu1/8.html':
        print('已到达第一章')
        print('保存成功')

        break
