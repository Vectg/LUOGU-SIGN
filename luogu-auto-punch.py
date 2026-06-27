# coding=utf-8
import json
import sys
from playwright.sync_api import sync_playwright, TimeoutError

def parse_cookie(cookie_str):
    """将Cookie字符串转换为Playwright所需格式"""
    cookies = []
    for item in cookie_str.strip(';').split(';'):
        if '=' not in item:
            continue
        name, value = item.split('=', 1)
        cookies.append({
            'name': name.strip(),
            'value': value.strip(),
            'domain': '.luogu.com.cn',
            'path': '/'
        })
    return cookies

def punch(cookie_str):
    with sync_playwright() as p:
        # 启动无头浏览器，移除自动化特征，降低被检测概率
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
        )
        # 创建浏览器上下文，模拟正常用户环境
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        # 预先注入登录Cookie
        context.add_cookies(parse_cookie(cookie_str))

        try:
            page = context.new_page()
            # 访问洛谷首页，等待DOM加载完成
            page.goto('https://www.luogu.com.cn', wait_until='domcontentloaded')

            # 等待CSRF Token元素出现，最多等30秒，预留Cloudflare验证时间
            page.wait_for_selector('meta[name="csrf-token"]', timeout=30000)
            csrf_token = page.locator('meta[name="csrf-token"]').get_attribute('content')
            print(f"成功获取CSRF Token: {csrf_token[:10]}...")

            # 复用当前浏览器会话发起打卡请求，Cookie/指纹完全一致
            response = context.request.post(
                'https://www.luogu.com.cn/index/ajax_punch',
                headers={
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'referer': 'https://www.luogu.com.cn/',
                    'x-csrf-token': csrf_token,
                    'x-requested-with': 'XMLHttpRequest'
                }
            )

            result_text = response.text()
            browser.close()
            return result_text

        except TimeoutError:
            browser.close()
            raise RuntimeError("页面加载超时，Cloudflare验证未通过（IP风控等级过高）")
        except Exception as e:
            browser.close()
            raise e

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
                sys.exit(1)
        except Exception as err:
            print(f"执行出错: {err}")
            sys.exit(1)
