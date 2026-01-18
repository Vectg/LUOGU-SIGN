import requests
import json
import sys

def punch(cookie):
    return requests.get('https://www.luogu.com.cn/index/ajax_punch', headers={
        "Host": "www.luogu.com.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv: 73.0) Gecko/20100101 Firefox/73.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.luogu.com.cn/",
        "Cache-Control": "no-cache",
        "TE": "Trailers",
        "Cookie": cookie
    }).text

if __name__ == "__main__":
    print(f"Script Name: {sys.argv[0]}")
    for i in range(1, len(sys.argv)):
        response = punch(sys.argv[i])
        print(f"No. {i}: {response}")
        try:
            tmp = json.loads(response)
            if tmp['code'] == 200:
                print('code =', tmp['code'], 'message =', tmp['more']['html'])
            else:
                print('code =', tmp['code'], 'message =', tmp['message'])
        except Exception as err:
            print(f"<{err}>")