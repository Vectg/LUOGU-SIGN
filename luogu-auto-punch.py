# coding=utf-8

import requests
import json
import sys

def GetCSRF(cookie):
    content = requests.get('https://www.luogu.com.cn', headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'content-length': '0',
        'origin': 'https://www.luogu.com.cn',
        'priority': 'u=1, i',
        'referer': 'https://www.luogu.com.cn/',
        'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Chrome',
        "Cookie": cookie
    }).content
    print(content)
    # soup = BeautifulSoup(content, 'html.parser')
    # token = soup.find('meta', {'name': 'csrf-token'})['content']
    p = content.find(b'csrf-token')
    token = content[p+21:p+76].decode('utf-8')
    print(token)
    return token

def punch(cookie):
    return requests.post('https://www.luogu.com.cn/index/ajax_punch', headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'content-length': '0',
        'origin': 'https://www.luogu.com.cn',
        'priority': 'u=1, i',
        'referer': 'https://www.luogu.com.cn/',
        'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Chrome',
        'x-csrf-token': GetCSRF(cookie),
        'x-requested-with': 'XMLHttpRequest',
        "Cookie": cookie
    }).text

if __name__ == "__main__":
    print(f"Script Name: {sys.argv[0]}")
    for i in range(1, len(sys.argv)):
        response = punch(sys.argv[i])
        print(f"No. {i}: {sys.argv[i]}")
        try:
            print(response)
            tmp = json.loads(response)
            if tmp['code'] == 200:
                print('code =', tmp['code'], 'message =', tmp['more']['html'])
            else:
                print('code =', tmp['code'], 'message =', tmp['message'])
        except Exception as err:
            print(f"<{err}>")
