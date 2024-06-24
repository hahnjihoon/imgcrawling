import os
import requests
from PIL import Image
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def auction(url, output_dir):
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

    iframe_element = driver.find_element(By.ID, "hIfrmExplainView")
    driver.switch_to.frame(iframe_element)  # iframe 내부로 전환
    page_source = driver.page_source
    root = HTMLParser(page_source)

    image_urls = []
    image_elements = root.css('#hdivDescription img')
    for image_element in image_elements:
        image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    for idx, image_url in enumerate(image_urls):
        try:
            img_data = requests.get(image_url).content
            with open(f'{title_dir}/image{idx}.jpg', 'wb') as f:
                f.write(img_data)
        except Exception as e:
            print(f"Error saving image {image_url}: {e}")

    print('auction 완료중')
    driver.quit()

    # 비교로직(원본이미지경로, 비교할이미지경로) 어떻게 실행할것인지?(다음이어서할지, rpa에서 로직돌릴지)
