# coding=utf-8
import cloudscraper
import json
import sys
import re

def GetCSRF(scraper):
    # 发起请求，自动处理 Cloudflare 挑战
    response = scraper.get('https://www.luogu.com.cn', headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'referer': 'https://www.luogu.com.cn/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    })
    
    # 正则匹配 csrf-token，比硬切片更稳定
    match = re.search(r'<meta name="csrf-token" content="([^"]+)">', response.text)
    if not match:
        raise RuntimeError("未能获取 CSRF Token，页面可能被 Cloudflare 拦截")
    
    token = match.group(1)
    print(f"获取到CSRF Token: {token[:10]}...")
    return token

def punch(cookie):
    # 创建 cloudscraper 实例
    scraper = cloudscraper.create_scraper()
    # 解析 cookie 并写入会话
    cookie_dict = {}
    for item in cookie.strip(';').split(';'):
        if '=' in item:
            k, v = item.split('=', 1)
            cookie_dict[k.strip()] = v.strip()
    scraper.cookies.update(cookie_dict)
    
    csrf_token = GetCSRF(scraper)
    
    resp = scraper.post(
        'https://www.luogu.com.cn/index/ajax_punch',
        headers={
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'referer': 'https://www.luogu.com.cn/',
            'x-csrf-token': csrf_token,
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }
    )
    return resp.text

if __name__ == "__main__":
    print(f"Script Name: {sys.argv[0]}")
    for i in range(1, len(sys.argv)):
        print(f"\n=== No. {i} ===")
        try:
            response = punch(sys.argv[i])
            print(response)
            tmp = json.loads(response)
            if tmp['code'] == 200:
                print('打卡成功！', tmp['more']['html'])
            else:
                print('打卡失败，code =', tmp['code'], '信息：', tmp['message'])
        except Exception as err:
            print(f"执行出错: {err}")
