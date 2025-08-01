import requests 
from lxml import etree
import os

url = 'https://www.99csw.com/book/2183/64857.htm'

headers = {
    'referer': 'https://www.99csw.com/book/2183/index.htm',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"138.0.7204.101"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.101", "Google Chrome";v="138.0.7204.101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"15.5.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

cookies = {
    'listpage': '1',
    '64857': '64',
    'PHPSESSID': 'hd0oi019i25enfup5qoj9lqn41',
    '_ga': 'GA1.1.1265517792.1752831958',
    'cf_clearance': 'bR19royuAhnzoplNbtuKLvk2MIFGTMsncLu6eqhgTdc-1752833661-1.2.1.1-eehZXs7HgJzqutQZ4.s8UrgVb0HW3727AA5vY2Kr4Yhe8zSzPJcRIkZzg4YW.fHoSndCp9Nc7mHTw0riLjpSfmF8qvk_JVvyoctuNHXo2arb7VdQNuf5RhibnhH3I3C.r7C0VtkXq23qlPySi_6qQcMlo0Yel5VNSNdRWoCjvwbzp8ti9v2ZABXZx5M.tVqbFIifb50XMhgHH_xrBCDtc3i1xKxhRbx2Czrw.ACn9.P2GdEnW8jO7QGG5YJ3ofns',
    '_ga_HCQ3NCRTVG': 'GS2.1.s1752831957$o1$g1$t1752833691$j17$l0$h0',
}

resp = requests.get(url, headers=headers, cookies=cookies)
resp.encoding = 'utf-8'
e = etree.HTML(resp.text)
title = e.xpath('//div[@id="content"]/h2/text()')
content = e.xpath('//div[@id="content"]/div/text()')

os.makedirs('射雕英雄传', exist_ok=True)  # 确保目录存在

print(resp)
# with open(f'{title}.txt','w', encoding='utf-8') as f:
#     f.write(title[0] + '\n')
#     for i in content:
#         f.write(i.strip() + '\n')

