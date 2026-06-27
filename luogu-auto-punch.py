import requests
import json
import sys
import re

# 强制 stdout 使用 UTF-8（解决 Windows 编码问题）
sys.stdout.reconfigure(encoding='utf-8')

def get_csrf_token(cookie):
    """从洛谷首页提取 CSRF token（正则匹配，更稳定）"""
    resp = requests.get('https://www.luogu.com.cn', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Cookie': cookie
    })
    match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', resp.text)
    if match:
        return match.group(1)
    else:
        raise RuntimeError("无法从页面提取 CSRF token，请检查网络或 Cookie 是否有效")

def punch(cookie):
    """执行签到请求"""
    token = get_csrf_token(cookie)
    resp = requests.post('https://www.luogu.com.cn/index/ajax_punch', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.luogu.com.cn/',
        'X-CSRF-Token': token,
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': cookie
    })
    return resp.text

if __name__ == "__main__":
    # 第一个参数是脚本名，后面每个参数是一个 Cookie 字符串（支持多账号）
    if len(sys.argv) < 2:
        print("❌ 错误：未提供 Cookie，请在 Secret 中设置 COOKIE")
        sys.exit(1)

    for i in range(1, len(sys.argv)):
        cookie = sys.argv[i].strip()
        print(f"正在签到账号 #{i} ...")
        try:
            response_text = punch(cookie)
            data = json.loads(response_text)
            if data.get('code') == 200:
                print(f"✅ 签到成功：{data['more']['html']}")
            else:
                print(f"❌ 签到失败：{data.get('code')} - {data.get('message', '未知错误')}")
        except Exception as e:
            print(f"⚠️ 账号 #{i} 出错：{e}")
