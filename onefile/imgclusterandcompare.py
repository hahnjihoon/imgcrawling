import os
from io import BytesIO
import re

import base64
import requests
from PIL import Image
from io import BytesIO

import requests
from PIL import Image
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json


def save_images(image_urls, title_dir):
    for index, image_url in enumerate(image_urls):
        try:
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            image_path = os.path.join(title_dir, f'image_{index}.jpg')
            image.save(image_path)
        except Exception as e:
            print(f"Error saving image {image_url}: {e}")

def save_image(url, path):
    try:
        if url.startswith("data:image"):
            header, encoded = url.split(",", 1)
            data = base64.b64decode(encoded)
            image = Image.open(BytesIO(data))
            image.save(path)
        else:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            if image.mode in ("RGBA", "P"):
                path = path.replace(".jpg", ".png")
            image.save(path)
    except Exception as e:
        print(f"Error saving image {url}: {e}")

def naver_save(image_urls, output_dir):
    for i, url in enumerate(image_urls):
        path = os.path.join(output_dir, f'image_{i}.png')  # Base64 이미지의 경우 PNG로 저장
        save_image(url, path)
    # for i, url in enumerate(urls):
    #     try:
    #         if isinstance(url, str) and url.startswith("data:image"):
    #             # Base64 인코딩된 이미지 처리
    #             header, encoded = url.split(",", 1)
    #             data = base64.b64decode(encoded)
    #             image = Image.open(BytesIO(data))
    #             image.save(os.path.join(path, f'image_{i}.png'))
    #         elif isinstance(url, str):
    #             # URL을 통한 이미지 처리
    #             response = requests.get(url)
    #             image = Image.open(BytesIO(response.content))
    #             if image.mode in ("RGBA", "P"):
    #                 image.save(os.path.join(path, f'image_{i}.png'))
    #             else:
    #                 image.save(os.path.join(path, f'image_{i}.jpg'))
    #     except Exception as e:
    #         print(f"Error saving image {url}: {e}")


def sanitize_title(title):
    # Windows 파일명에 사용할 수 없는 문자를 제거합니다.
    return re.sub(r'[\/:*?"<>|]', '', title)


def auction(url, output_dir):
    print(f"auction: {url}, {output_dir}")
    print('auction fine :: ', url)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # 제목 추출
    title_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.itemtit'))
    )
    title = title_element.text.strip()
    print('Title:', title)

    first_slash_index = title.find('/')
    if first_slash_index != -1:
        # 첫 번째 슬래시 이전의 문자열 추출
        title = title[:first_slash_index]

    # 제목 폴더 생성
    title_dir = os.path.join(output_dir, title)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)

    # 옥션에만있는 상세보기버튼클릭
    detail_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.js-toggle-button'))
    )
    detail_button.click()

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    # 실제 iframe안에 상태 이미지가 있으므로
    iframe_element = driver.find_element(By.ID, "hIfrmExplainView")
    driver.switch_to.frame(iframe_element)  # iframe 내부로 전환
    page_source = driver.page_source
    root = HTMLParser(page_source)

    image_urls = []
    image_elements = root.css('#hdivDescription img')
    for image_element in image_elements:
        image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    save_images(image_urls, title_dir)

    print('auction 완료중')
    driver.quit()


def elevenst(url, output_dir):
    print(f"elevenst: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    # h1 태그에서 제목 추출
    title_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.title'))
    )
    title = title_element.text.strip()
    print('Title:', title)

    first_slash_index = title.find('/')
    if first_slash_index != -1:
        # 첫 번째 슬래시 이전의 문자열 추출
        title = title[:first_slash_index]

    # 제목 폴더 생성
    title_dir = os.path.join(output_dir, title)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)

    # 실제 iframe안에 상태 이미지가 있으므로 iframe으로 전환
    iframe_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "prdDescIfrm"))
    )
    driver.switch_to.frame(iframe_element)

    page_source = driver.page_source
    root = HTMLParser(page_source)

    # 이미지 URL 추출
    image_urls = []
    image_elements = root.css('img')
    for image_element in image_elements:
        if 'src' in image_element.attributes:
            image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    # 이미지 저장
    save_images(image_urls, title_dir)

    print('eleven 완료중')
    driver.quit()


def gmarket(url, output_dir):
    print(f"gmarket: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    # h1 태그에서 제목 추출
    title_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.itemtit'))
    )
    title = title_element.text.strip()
    print('Title:', title)

    first_slash_index = title.find('/')
    if first_slash_index != -1:
        # 첫 번째 슬래시 이전의 문자열 추출
        title = title[:first_slash_index]

    # 제목 폴더 생성
    title_dir = os.path.join(output_dir, title)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)

    # 실제 iframe안에 상태 이미지가 있으므로 iframe으로 전환
    iframe_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "detail1"))
    )
    driver.switch_to.frame(iframe_element)

    page_source = driver.page_source
    root = HTMLParser(page_source)

    # 이미지 URL 추출
    image_urls = []
    image_elements = root.css('img')
    for image_element in image_elements:
        if 'src' in image_element.attributes:
            image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    # 이미지 저장
    save_images(image_urls, title_dir)

    print('gmarket 완료중')
    driver.quit()


def naver_login(driver):
    print('111111111111111')
    driver.get('https://nid.naver.com/nidlogin.login')
    print('22222222222222')
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#id'))
    )
    print('33333333333333333333')

    # 네이버 아이디와 비밀번호를 입력합니다
    username = 'hahnjh0426'
    password = '1q2w3e4r!!'

    driver.find_element(By.CSS_SELECTOR, 'input#id').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input#pw').send_keys(password)

    driver.find_element(By.CSS_SELECTOR, 'button.btn_login').click()
    print('444444444444444444444444')

    # 로그인 후 페이지 로드 대기
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
    )


def naver(url, output_dir):
    print(f"naver: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-webgl')
    driver = webdriver.Chrome(options=options)

    naver_login(driver)

    driver.get(url)

    # cookies = driver.get_cookies()
    # print("Session cookies:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    # for cookie in cookies:
    #     print(cookie)

    try:
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h3._22kNQuEXmb._copyable'))  # 상품제목 태그클래스명
        )
        title = title_element.text.strip()
    except TimeoutException:
        print("Title element not found, trying another selector")
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h2._1Y6hi'))  # 이런게 없긴함
        )
        title = title_element.text.strip()

    print('Title:', title)

    title = sanitize_title(title)
    title_dir = os.path.join(output_dir, title)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)

    print('33333333333333333')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
    )

    # print('44444444444444444444444444444444')
    # page_source = driver.page_source
    # root = BeautifulSoup(page_source, 'html.parser')
    # print('루트:: ', root)

    #셀리니움으로 클릭
    # print('5555555555555555555555555555555')
    # button = root.select_one('._1gG8JHE9Zc._nlog_click')
    # print('77777777777777777777777777777777777')
    # if button:
    #     button_id = button.get('id')
    #     if button_id:
    #         # JavaScript를 사용하여 버튼 클릭
    #         print('id있어')
    #         driver.execute_script(f"document.getElementById('{button_id}').click()")
    #     else:
    #         # 버튼 요소가 id가 없는 경우, 다른 방법으로 클릭 시도
    #         print('id없어')
    #         driver.execute_script("arguments[0].click();", button)
    # print('66666666666666666666666666666666')

    #뷰티풀로 클릭
    # button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, '._1gG8JHE9Zc._nlog_click'))
    # )
    #
    # # 추가적인 정보 제공 (예: 쿠키)
    # cookies = driver.get_cookies()
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    #
    # # 버튼 클릭
    # button.click()
    print('44444444444444444444444')
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#INTRODUCE > div > div:nth-child(5) > button'))
    )
    print('555555555555555555555555555')
    search_box.click()
    print('666666666666666666666666666')

    time.sleep(2)
    print('버튼 클릭 성공')

    #상세버튼 눌러서 새로운태그 생성시키고 다시가져와
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
    )

    page_source2 = driver.page_source
    root2 = BeautifulSoup(page_source2, 'html.parser')
    print('root2222::', root2)

    image_urls = []
    a_tags = root2.find_all('a', class_='se-module-image-link-use se-module-image-link __se_image_link __se_link')
    for a_tag in a_tags:
        data_linkdata = a_tag.get('data-linkdata')
        if data_linkdata:
            data = json.loads(data_linkdata)
            image_src = data.get('src')
            if image_src:
                print(f"Image src: {image_src}")
                image_urls.append(image_src)

    # 이미지 src 추출
    # 클래스명이 basic_detail_html인 div 안의 모든 img 태그의 src 추출
    # image_urls = []
    # # image_elements = root2.select('#SE-dfb29804-23b5-4a02-9e50-56610c18adaf img')
    # image_elements = root2.select('#SE-9ed78a54-e7c9-4001-9175-779e02fc6751 img')
    # for image_element in image_elements:
    #     if 'src' in image_element.attrs:
    #         image_urls.append(image_element['src'])

    print('get image_urls', image_urls)

    # 이미지 저장
    save_images(image_urls, title_dir)

    print('naver 완료중')
    driver.quit()


def image_crawling(paramlist):
    if len(paramlist) != 3:
        print("Error: 필수 파라미터를 확인하세요")
        return

    # AA에서 파라미터 리스트로넘겨줌
    commerce_code = paramlist[0]  # 첫 번째 파라미터: 커머스코드
    img_url = paramlist[1]  # 두 번째 파라미터: 이미지url
    save_path = paramlist[2]  # 세 번째 파라미터: 저장장소

    print(f'커머스코드: {commerce_code}')
    print(f'이미지url: {img_url}')
    print(f'저장장소: {save_path}')

    commerce_code = commerce_code.lower()  # 무조건소문자
    if commerce_code == 'auction':
        auction(img_url, save_path)

    if commerce_code == 'elevenst':
        elevenst(img_url, save_path)

    if commerce_code == 'gmarket':
        gmarket(img_url, save_path)

    if commerce_code == 'naver':
        naver(img_url, save_path)


# 로컬에서 실행test
if __name__ == "__main__":
    a = 'naver'
    b = 'https://brand.naver.com/cj_wellcare/products/9954053367'
    c = "C:/Users/Rainbow Brain/Desktop/save"
    param = [a, b, c]

    image_crawling(param)
