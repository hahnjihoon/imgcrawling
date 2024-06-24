import subprocess
import time
import random
import asyncio
import aiohttp
import requests
from fetch import Fetch
from selectolax.parser import HTMLParser
import os
import requests
from PIL import Image
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# def get_current_ip():
#     try:
#         response = requests.get('http://api.ipify.org?format=json')
#         ip = response.json()['ip']
#         print(f"현재 IP 주소: {ip}")
#         return ip
#     except Exception as e:
#         print(f"IP 주소를 가져오는 데 실패했습니다: {e}")
#         return None
#
#
# async def fetch_data():
#     exe_path = "C:/Program Files/OpenVPN/bin/openvpn-gui.exe"
#
#     # VPN 연결 시작
#     asdfee = subprocess.call([r'C:\imgcrawling\ovpn_connect.bat'])
#     print('11', asdfee)
#
#     print('bat파일로 연결됨')
#     time.sleep(10)
#
#     # 현재 IP 주소 가져오기
#     get_current_ip()
#
#     REQUEST_HEADERS = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                       "Chrome/90.0.4430.93 Safari/537.36",
#     }
#     COOKIES = {
#         "PCID": "15572593772180093402940",
#     }
#     LINK = "https://www.coupang.com/vp/products/328677319?itemId=1051091399"
#     sleep_time = random.uniform(1, 3)
#     time.sleep(sleep_time)
#     print('쿠팡 시작점')
#
#     async with aiohttp.ClientSession(headers=REQUEST_HEADERS, cookies=COOKIES) as session:
#         async with session.get(LINK) as response:
#             return await response.text()
#
#
# async def main():
#     try:
#         # fetch_data를 15초 동안만 기다림
#         result = await asyncio.wait_for(fetch_data(), timeout=60.0)
#         print(result)
#     except asyncio.TimeoutError:
#         print('응답 시간이 60초를 초과했습니다.')
#     finally:
#         # VPN 연결 해제
#         subprocess.call([r'C:\imgcrawling\ovpn_disconnect.bat'])
#         print('VPN 연결 해제됨.')
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

def get_current_ip():
    try:
        response = requests.get('http://api.ipify.org?format=json')
        ip = response.json()['ip']
        print(f"현재 IP 주소: {ip}")
        return ip
    except Exception as e:
        print(f"IP 주소를 가져오는 데 실패했습니다: {e}")
        return None


async def fetch_data():
    exe_path = "C:/Program Files/OpenVPN/bin/openvpn-gui.exe"

    # VPN 연결 시작
    process = await asyncio.create_subprocess_exec(r'C:\imgcrawling\ovpn_connect.bat')
    await process.communicate()
    print('bat파일로 연결됨')

    await asyncio.sleep(10)  # 비동기 대기

    # 현재 IP 주소 가져오기
    get_current_ip()

    REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.93 Safari/537.36",
    }
    COOKIES = {
        "PCID": "15572593772180093402940",
    }
    LINK = "https://www.coupang.com/vp/products/328677319?itemId=1051091399"
    # LINK = "https://www.naver.com"
    sleep_time = random.uniform(1, 3)
    await asyncio.sleep(sleep_time)  # 비동기 대기
    print('쿠팡 시작점')

    # 내코드
    # async with aiohttp.ClientSession(headers=REQUEST_HEADERS, cookies=COOKIES) as session:
    #     async with session.get(LINK) as response:
    #         return await response.text()

    # 기존쿠팡
    # res = await Fetch.get(
    #     LINK, skip_auto_headers=REQUEST_HEADERS, cookies=COOKIES
    # )
    # root = HTMLParser(res)
    # script = None
    # for node in root.css('body > script'):
    #     if '__PRELOADED_STATE__' in node.text():
    #         script = node.text()
    #         print(script)
    #         print('됐다------------------------------------------------------------------------------------------------')
    #         break
    #
    #     if script is None:
    #         print('스크립트없을때 돈다')
    #         break

    #셀레
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(LINK)
    try:  # 수정된 부분 시작
        title_element = WebDriverWait(driver, 59).until(  # 시간을 늘렸습니다.
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.prod-buy-header__title'))
        )
        title = title_element.text.strip()
        print('Title:', title)
    except Exception as e:
        print(f"제목을 찾는 동안 에러가 발생했습니다: {e}")
    finally:
        driver.quit()  # 수정된 부분 끝

async def main():
    try:
        # fetch_data를 60초 동안만 기다림
        result = await asyncio.wait_for(fetch_data(), timeout=60.0)
        print(result)
    except asyncio.TimeoutError:
        print('응답 시간이 60초를 초과했습니다.')
    finally:
        # VPN 연결 해제
        process = await asyncio.create_subprocess_exec(r'C:\imgcrawling\ovpn_disconnect.bat')
        await process.communicate()
        print('VPN 연결 해제됨.')
        get_current_ip()


if __name__ == "__main__":
    asyncio.run(main())
