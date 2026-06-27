import requests
import json
import sys

# 强制 stdout 使用 UTF-8，避免 Windows 控制台编码错误
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def punch(cookie):
    return requests.get('https://www.luogu.com.cn/index/ajax_punch', headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv: 73.0) Gecko/20100101 Firefox/73.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Referer": "https://www.luogu.com.cn/",
        "Cookie": cookie
    }).text

if __name__ == "__main__":
    # 不再打印脚本名和 cookie 内容
    for i in range(1, len(sys.argv)):
        cookie = sys.argv[i]
        print(f"正在签到账号 #{i} ...")
        response = punch(cookie)
        try:
            tmp = json.loads(response)
            if tmp.get('code') == 200:
                print(f"✅ 签到成功：{tmp['more']['html']}")
            else:
                print(f"❌ 签到失败：{tmp.get('code')} - {tmp.get('message', '未知错误')}")
        except Exception as err:
            print(f"⚠️ 解析响应出错：{err}")
