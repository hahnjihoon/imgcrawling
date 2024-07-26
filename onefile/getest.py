import base64
import os
from io import BytesIO
import requests
from PIL import Image
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import etree
import traceback
import pyautogui
import pyperclip

def gsshop(url, output_dir):
    print(f"gsshop: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    driver = initialize_and_open_url(url)
    if driver is None:
        return

    try:
        # ID로 CSS를 찾는거라 기존함수 못돌림, 이것하나때문에 새함수 작성불가
        gsshop_class = 'prdDetailIfr'  # 여기에 찾아야할 상위태그의 ID값 수정

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, gsshop_class))
        )
        driver.switch_to.frame(element)

        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        collections = root.css('span, p')
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa',len(collections))
        for collection_index, collection in enumerate(collections): #인덱스와 함께반환하는함수
            tag_name = collection.tag  # 현재 태그 이름을 가져옴

            print('--------------------시작------------------------------------------------------------------------')
            print("Collection HTML: ", collection.html)  # 각 태그의 HTML 내용을 출력
            print(f"지금태그 {tag_name} tag at index {collection_index}")

            image_urls = []  #span 이나 p 안의 img모음
            image_elements = collection.css('img')
            for image_element in image_elements:
                image_urls.append(image_element.attributes['src'])
            print("완성된 span,p 안의 img url들:: ", image_urls) #span이나p안의 img다 담았어

            # 이미지를 합쳐서 저장하는 부분
            from PIL import Image
            import requests
            from io import BytesIO

            images = []
            for url in image_urls: #다담은거에서 1개씩 루프
                try:
                    response = requests.get(url)
                    img = Image.open(BytesIO(response.content))
                    images.append(img) #byte로 이미지를 리스트에 담아
                except Exception as e:
                    print(f"Error loading image from {url}: {e}")

            if images:
                # 이미지를 세로로 합치기
                widths, heights = zip(*(i.size for i in images))
                total_height = sum(heights)
                max_width = max(widths)
                # 길이 추출해서 가로세로템플릿만들어둠
                combined_image = Image.new('RGB', (max_width, total_height))
                y_offset = 0 #y시작위치
                for img in images:
                    combined_image.paste(img, (0, y_offset))
                    y_offset += img.height

                # 저장 경로 설정
                collection_name = f"수집{collection_index}"
                combined_image_path = os.path.join(output_dir, f"{collection_name}.jpg")
                combined_image.save(combined_image_path)
                print(f"합치고 저장이름 as {combined_image_path}")
                print('===========================================끝===============================================')
            else:
                print(f"No images found for collection {collection_index}")



    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    print('gsshop 완료중')
    driver.quit()