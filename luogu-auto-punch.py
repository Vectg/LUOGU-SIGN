# coding=utf-8
import requests
import json
import sys
import re

def GetCSRF(cookie):
    # 1. 使用 .text 让 requests 自动处理编码
    # 2. 精简请求头，只保留必要的
    response = requests.get('https://www.luogu.com.cn', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        "Cookie": cookie
    })
    response.encoding = 'utf-8' # 确保编码为UTF-8
    
    # 使用正则表达式提取 CSRF Token
    match = re.search(r'<meta name="csrf-token" content="([^"]+)"', response.text)
    if match:
        token = match.group(1)
        print("CSRF Token 获取成功")  # 不打印 token 本身，避免泄露
        return token
    else:
        raise Exception("未能在页面中找到 CSRF Token，请检查 Cookie 是否有效或页面结构是否变化")

def punch(cookie):
    token = GetCSRF(cookie)
    response = requests.post('https://www.luogu.com.cn/index/ajax_punch', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.luogu.com.cn/',
        'X-CSRF-Token': token,
        'X-Requested-With': 'XMLHttpRequest',
        "Cookie": cookie
    })
    return response.text

if __name__ == "__main__":
    # 不打印脚本名和cookie，保护隐私
    for i in range(1, len(sys.argv)):
        cookie = sys.argv[i]
        print(f"正在为账号 #{i} 执行签到...")
        try:
            response = punch(cookie)
            tmp = json.loads(response)
            if tmp['code'] == 200:
                print(f'✅ 签到成功：{tmp["more"]["html"]}')
            else:
                print(f'❌ 签到失败：{tmp["code"]} - {tmp["message"]}')
        except Exception as err:
            print(f"⚠️ 账号 #{i} 签到过程发生错误：{err}")
