import os

from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pyautogui
import requests
from selectolax.parser import HTMLParser
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

options = Options()
options.add_argument("--start-maximized")

# touchvpn_extension_id = "bihmplhobchoageeokmgbdihknkjbknd"

options.add_extension("C:/BIHMPLHOBCHOAGEEOKMGBDIHKNKJBKND_5_0_18_0.crx")

driver = webdriver.Chrome(options=options)
print('유지')
time.sleep(5)
print('좌표')
# try:
#     while True:
#         # 현재 마우스의 위치를 가져와서 출력합니다.
#         x, y = pyautogui.position()
#         print(f"마우스 위치: x={x}, y={y}", end='\r')  # 매번 줄 바꿈 없이 출력합니다.
#
# except KeyboardInterrupt:
#     print("\n종료되었습니다.")

def click_coordinates():
    try:
        # 첫 번째 좌표 클릭 (1807, 611)
        pyautogui.click(1807, 50)
        print("좌표를 클릭했습니다.")
        time.sleep(3)  # 3초 대기

        # 두 번째 좌표 클릭 (1682, 218)
        pyautogui.click(1682, 200)
        print("좌표를 클릭했습니다.")
        time.sleep(4)  # 3초 대기

        # 세 번째 좌표 클릭 (1602, 377)
        pyautogui.click(1600, 380)
        print("좌표를 클릭했습니다.")

        # 5초 대기
        print("5초 대기 중...")
        time.sleep(5)

    except KeyboardInterrupt:
        print("종료되었습니다.")


file_path = "C:/Users/Rainbow Brain/Desktop/PEB04_Coupang_Result_DB.xlsx"
sheet_name = '가격순위'
data = pd.read_excel(file_path, header=0, sheet_name=sheet_name)

urls = data['url']

click_coordinates()

# 페이지로 이동
print('이거나오면 드라이버주소이동')
for i, url in enumerate(urls):
    print(f'{i + 1}번째::{url}')
    try:
        driver.get(url)
        time.sleep(5)  # 기본 대기 시간

        # 웹 페이지가 완전히 로드될 때까지 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.prod-buy-header__title')))

        # 페이지 소스를 가져와서 BeautifulSoup으로 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        error_page = soup.select_one('div.error-page')
        if error_page and error_page.text.strip():
            print(f"Error page detected at {url}. Restarting clicks...")
            click_coordinates()
            break

        # Title 요소 추출
        title_element = soup.select_one('h2.prod-buy-header__title')
        if title_element:
            title = title_element.text.strip()
            print('Title:', title)
        else:
            print('Title element not found.')

        # Brand 요소 추출
        brand_element = soup.select_one('a.prod-brand-name')
        if brand_element:
            brand = brand_element.text.strip()
            print('Brand:', brand)
        else:
            print('Brand element not found.')

    except Exception as e:
        print(f'Attempt failed: {e}')

    # input('쿠팡완료 엔터입력')

#########################################이걸로 대입시킬것 월 ##########################################################
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time
#
# # 데이터프레임에서 URL 추출
# data = pd.read_excel('data.xlsx')  # 엑셀 파일에서 데이터프레임으로 불러오기
# urls = data['url'].tolist()  # URL 리스트로 변환
#
# # Selenium WebDriver 설정
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않음
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
#
# service = Service('/path/to/chromedriver')  # 크롬드라이버 경로 설정
# driver = webdriver.Chrome(service=service, options=chrome_options)
#
# # 각 URL에 대해 HTML 파싱
# for url in urls:
#     try:
#         driver.get(url)  # URL로 이동
#         # 페이지 로딩이 완료될 때까지 대기
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
#
#         # 페이지의 HTML을 가져와서 BeautifulSoup으로 파싱
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#
#         # HTML 출력 (또는 원하는 다른 처리)
#         print(soup.prettify())
#
#     except Exception as e:
#         print(f"Error occurred for URL {url}: {e}")
#         continue
#
# # WebDriver 종료
# driver.quit()
######################################################################################################################

# driver.quit()


# title_element = WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.prod-buy-header__title'))
# )
# title = title_element.text.strip()
# print('Title:', title)
#
# # brand_ele = WebDriverWait(driver, 3).until(
# #     EC.presence_of_element_located((By.CSS_SELECTOR, 'a.prod-brand-name'))
# # )
# # brand = brand_ele.text.strip()
# # print('Title:', brand)

