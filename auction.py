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
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # url = "http://itempage3.auction.co.kr/DetailView.aspx?itemno=C499114079"
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    detail_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.js-toggle-button')))
    detail_button.click()

    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    iframe_element = driver.find_element(By.ID, "hIfrmExplainView")
    driver.switch_to.frame(iframe_element)  # iframe 내부로 전환
    page_source = driver.page_source
    root = HTMLParser(page_source)

    image_urls = []
    image_elements = root.css('#hdivDescription img')
    for image_element in image_elements:
        image_urls.append(image_element.attributes['src'])

    print('1111111111111111111111111', image_urls)

    for idx, image_url in enumerate(image_urls):
        img_data = requests.get(image_url).content
        with open(f'{output_dir}/image{idx}.jpg', 'wb') as f:
            f.write(img_data)

    image_list = [f'{output_dir}/image{idx}.jpg' for idx in range(len(image_urls))]

    print('22222222222222222222222', image_list)

    output_path = f"{output_dir}/merged_image.png"
    images = [Image.open(i) for i in image_list]

    print('33333333333', images)

    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    total_height = sum(heights)
    combined_image = Image.new('RGB', (max_width, total_height), color='white')
    y_offset = 0
    for im in images:
        combined_image.paste(im, (0, y_offset))
        y_offset += im.size[1]  # 0가로 1세로
    combined_image.save(output_path, ptimize=True, quality=10, compress_level=9)
    driver.quit()
