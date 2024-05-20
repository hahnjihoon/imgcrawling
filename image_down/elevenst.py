import os
from io import BytesIO

import requests
from PIL import Image
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def elevenst(url, output_dir):
    print('eleven fine :: ', url)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

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

    # iframe으로 전환
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
    for index, image_url in enumerate(image_urls):
        try:
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            image_path = os.path.join(title_dir, f'image_{index}.jpg')
            image.save(image_path)
        except Exception as e:
            print(f"Error saving image {image_url}: {e}")

    print('eleven 완료중')
    driver.quit()