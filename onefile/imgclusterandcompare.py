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


def find_element_class(driver, selectors):
    loop_count = 0
    for selector in selectors:
        loop_count += 1
        print(f"Trying selector {loop_count}: {selector}")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return driver.find_element(By.CSS_SELECTOR, selector)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Selector {selector} not found. Exception: {e}")
            pass
    raise NoSuchElementException(f"None of the selectors were found: {selectors}")


def find_element_id(driver, selectors):
    loop_count = 0
    for selector in selectors:
        loop_count += 1
        print(f"Trying selector {loop_count}: {selector}")
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, selector)))
            iframe_element = driver.find_element(By.ID, selector)
            return driver.switch_to.frame(iframe_element)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Selector {selector} not found. Exception: {e}")
            pass
    raise NoSuchElementException(f"None of the selectors were found: {selectors}")


def save_images(image_urls, title_dir):
    # 저장할 디렉토리가 존재하지 않으면 생성
    if not makedir(title_dir):
        return

    for index, image_url in enumerate(image_urls):
        try:
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))

            if image.format == 'GIF':
                image_path = os.path.join(title_dir, f'수집{index}.gif')
                image.save(image_path, save_all=True)
            else:
                if image.mode == 'P' or image.mode == 'RGBA':
                    image = image.convert('RGB')
                image_path = os.path.join(title_dir, f'수집{index}.jpg')
                image.save(image_path, 'JPEG')

            print(f"Saved image: {image_path}")

        except Exception as e:
            print(f"Error saving image {image_url}: {e}")
            traceback.print_exc()


def makedir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        traceback.print_exc()
        return False
    return True


def initialize_and_open_url(url):
    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver or opening URL {url}: {e}")
        traceback.print_exc()
        return None


def auction(url, output_dir):
    print(f"auction: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    driver = initialize_and_open_url(url)
    if driver is None:
        return

    # 옥션에만있는 상세보기버튼클릭
    try:
        detail_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.js-toggle-button'))
        )
        detail_button.click()
    except Exception as e:
        print(f"Error clicking detail button: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
    except Exception as e:
        print(f"Error waiting for body to load: {e}")
        traceback.print_exc()
        driver.quit()
        return

    # 실제 iframe안에 상태 이미지가 있으므로
    # iframe_element = driver.find_element(By.ID, "hIfrmExplainView")
    # driver.switch_to.frame(iframe_element)  # iframe 내부로 전환
    try:
        auction_class = ['.testest', 'hIfrmExplainView']
        find_element_id(driver, auction_class)
    except Exception as e:
        print(f"Error finding iframe: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        image_elements = root.css('#hdivDescription img')
        for image_element in image_elements:
            image_urls.append(image_element.attributes['src'])
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('auction 완료중')
    driver.quit()


def elevenst(url, output_dir):
    print(f"elevenst: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    driver = initialize_and_open_url(url)
    if driver is None:
        return

    try:
        eleven_class = ['.3dkeje', 'prdDescIfrm']
        find_element_id(driver, eleven_class)
    except Exception as e:
        print(f"Error finding iframe: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        image_elements = root.css('img')
        for image_element in image_elements:
            image_urls.append(image_element.attributes['src'])
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('eleven 완료중')
    driver.quit()


def gmarket(url, output_dir):
    print(f"gmarket: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    driver = initialize_and_open_url(url)
    if driver is None:
        return

    try:
        gmarket_class = ['test', 'detail1']
        find_element_id(driver, gmarket_class)
    except Exception as e:
        print(f"Error finding iframe: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        image_elements = root.css('img')
        for image_element in image_elements:
            image_urls.append(image_element.attributes['src'])
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('gmarket 완료중')
    driver.quit()


def naver_login(driver):
    driver.get('https://nid.naver.com/nidlogin.login')
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#id'))
    )

    # 네이버 아이디와 비밀번호를 입력합니다
    username = 'asdf'
    password = 'asdf!!'

    driver.find_element(By.CSS_SELECTOR, 'input#id').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input#pw').send_keys(password)

    driver.find_element(By.CSS_SELECTOR, 'button.btn_login').click()

    # 로그인 후 페이지 로드 대기
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
    )


def naver_brand(url, output_dir):
    print(f"naver_brand: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    try:
        options = Options()
        # options.add_argument('--headless') #네이버는 화면을 켜야됨 = rpa가 하는게 나음
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-webgl')
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        traceback.print_exc()
        return

    # naver_login(driver) #로그인 시키기

    try:
        driver.get(url)
    except Exception as e:
        print(f"Error opening URL {url}: {e}")
        traceback.print_exc()
        driver.quit()
        return

    # 로그인 쿠키사용할때의 로직(현재 사용안함)
    # cookies = driver.get_cookies()
    # print("Session cookies:::::::::::::::::::::::::::::::::::::::")
    # for cookie in cookies:
    #     print(cookie)

    print('버튼클릭전')  # 화면자체를 켜서 눌러야됨 코드상으로는 api를 호출해서 검증하는듯 그래서 안됨
    try:
        button_xpath = '//*[@id="INTRODUCE"]/div/div[5]/button'
        button_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, button_xpath))
        )
        button_element.click()
        time.sleep(2)
        print('버튼 클릭 성공')
    except Exception as e:
        print(f"Error clicking detail button: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
    except Exception as e:
        print(f"Error waiting for body to load: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        # 이미지파싱도 일부분은 javascript를 사용해서 구현하는듯, 그래서 https가 아닌 이미지url이 나옴 = 그런건 저장안됨
        image_urls = []
        image_elements = root.css(
            '#INTRODUCE > div > div._3osy73V_eD._1Hc_ju_IXp._2pWm5xPRcr > div:nth-child(1) > div:nth-child(2) > div._9F9CWn02VE > div > div > div > div img')

        for image_element in image_elements:
            if 'src' in image_element.attributes:
                src = image_element.attributes['src']
                if not src.startswith('h'):
                    data_src = image_element.attributes['data-src']
                    image_urls.append(data_src)
                else:
                    image_urls.append(src)
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('naver-brand 완료중')
    driver.quit()


def naver_search_shopping(url, output_dir):
    print(f"naver_search_shopping: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    try:
        options = Options()
        # options.add_argument('--headless') #네이버는 화면을 켜야됨 = rpa가 하는게 나음
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-webgl')
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        traceback.print_exc()
        return

    try:
        driver.get(url)
    except Exception as e:
        print(f"Error opening URL {url}: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        # naver_shop_class = ['.additionalImages_export_atc__XVRNd'] #정상클래스
        naver_shop_class = ['.specInfo_section_spec__CApfx']  # 상위클래스 // 자바스크립트때문에 하위가 안잡힘
        # 이url은 rpa로 해야할듯 // 현재 모든이미지 다긁어옴
        find_element_class(driver, naver_shop_class)
        page_source = driver.page_source
        root = HTMLParser(page_source)
        # print('root:: ', root.text())
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        # image_elements = root.css('.additionalImages_product_img__ALP0s img')
        image_elements = root.css('img')
        for image_element in image_elements:
            if 'src' in image_element.attributes:
                image_urls.append(image_element.attributes['src'])
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('naver_search_shopping 완료중')
    driver.quit()


def ssg(url, output_dir):
    print(f"ssg: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        traceback.print_exc()
        return

    try:
        driver.get(url)
    except Exception as e:
        print(f"Error opening URL {url}: {e}")
        traceback.print_exc()
        driver.quit()
        return

    # ssg에만있는 상세보기버튼클릭
    try:
        detail_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.ctrl_collapse'))
        )
        detail_button.click()
    except Exception as e:
        print(f"Error clicking detail button: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
    except Exception as e:
        print(f"Error waiting for body to load: {e}")
        traceback.print_exc()
        driver.quit()
        return

    # 실제 iframe안에 상태 이미지가 있으므로
    # iframe_element = driver.find_element(By.ID, "_ifr_html")
    # driver.switch_to.frame(iframe_element)  # iframe 내부로 전환
    try:
        ssg_class = ['test', '_ifr_html']
        find_element_id(driver, ssg_class)
    except Exception as e:
        print(f"Error finding iframe: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        image_elements = root.css('img')
        for image_element in image_elements:
            image_urls.append(image_element.attributes['src'])
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('ssg 완료중')
    driver.quit()


def cjthemarket(url, output_dir):
    print(f"cjthemarket: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    driver = initialize_and_open_url(url)
    if driver is None:
        return

    # cj the market은 상세보기버튼없이 펼쳐져있음
    try:
        cjthemarket_class = ['.product-detail']
        find_element_class(driver, cjthemarket_class)
    except Exception as e:
        print(f"Error finding iframe: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        # div 클래스명프로덕트디테일하위의 img다 찾으란소리, 이거말고 아예 필요이미지만 있는 상위 div클래스명 필요
        # 찾기힘들면 selector 복사하면됨
        image_elements = root.css(
            '#prdDetail > div.product-detail-images.mt40.slick-initialized.slick-slider.slick-dotted > div.slick-list > div > div:nth-child(3) img')

        # cjthemarket은 src에 http:가 쳐 빠져있음 붙여서 리스트업
        for image_element in image_elements:
            # src 속성을 가져와서 앞에 http: 붙이기
            url = 'http:' + image_element.attributes['src']
            image_urls.append(url)
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('cj the market 완료중')
    driver.quit()


def hmall(url, output_dir):
    print(f"hmall: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    driver = initialize_and_open_url(url)
    if driver is None:
        return

    try:
        hmall_class = ['.view-content']
        find_element_class(driver, hmall_class)
    except Exception as e:
        print(f"Error finding iframe: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        image_elements = root.css(
            '.view-content img')
        for image_element in image_elements:
            image_urls.append(image_element.attributes['src'])
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('hmall 완료중')
    driver.quit()


def lotteon(url, output_dir):
    print(f"lotteon: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    driver = initialize_and_open_url(url)
    if driver is None:
        return

    # lotteon에만있는 상세보기버튼클릭
    try:
        detail_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.hasIcon.strokeRed.more.sizeMedium.alignRight'))
        )
        detail_button.click()
    except Exception as e:
        print(f"Error clicking detail button: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
    except Exception as e:
        print(f"Error waiting for body to load: {e}")
        traceback.print_exc()
        driver.quit()
        return

    # 실제 iframe안에 상태 이미지가 있으므로
    # iframe_element = driver.find_element(By.ID, "_ifr_html")
    # driver.switch_to.frame(iframe_element)  # iframe 내부로 전환
    try:
        lotteon_class = ['m2-prd-frame']  # 아이디일땐 그냥 아이디값만
        find_element_id(driver, lotteon_class)
    except Exception as e:
        print(f"Error finding iframe: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        image_elements = root.css('img')
        for image_element in image_elements:
            image_urls.append(image_element.attributes['src'])
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('lotteon 완료중')
    driver.quit()


def cjonstyle(url, output_dir):
    print(f"cjonstyle: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    driver = initialize_and_open_url(url)
    if driver is None:
        return

    try:
        cjonstyle_class = ['#_itemExplainAreaInfoIframe > iframe']
        resutl = find_element_class(driver, cjonstyle_class)
        driver.switch_to.frame(resutl)
    except Exception as e:
        print(f"Error finding iframe: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        image_elements = root.css('img')
        for image_element in image_elements:
            if 'src' in image_element.attributes:
                src = image_element.attributes['src']
                if src.startswith('//'):
                    image_url = 'http:' + src
                elif not src.startswith('http'):
                    image_url = 'http://' + src
                else:
                    image_url = src
                image_urls.append(image_url)
        print('get image_urls', image_urls)
        # 현커머스는 css로 찾고 그걸 iframe으로 변환시키고 가져온 src를 가공해야 다운가능
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('cjonstyle 완료중')
    driver.quit()


def emartmall(url, output_dir):
    print(f"emartmall: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    driver = initialize_and_open_url(url)
    if driver is None:
        return

    # emartmall 상세보기버튼클릭
    try:
        detail_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_collapse.ctrl_collapse'))
        )
        detail_button.click()
    except Exception as e:
        print(f"Error clicking detail button: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
    except Exception as e:
        print(f"Error waiting for body to load: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        emartmall_class = ['_ifr_html']  # 아이디일땐 그냥 아이디값만
        find_element_id(driver, emartmall_class)
    except Exception as e:
        print(f"Error finding iframe: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        image_elements = root.css('img')
        for image_element in image_elements:
            image_urls.append(image_element.attributes['src'])
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('emartmall 완료중')
    driver.quit()


def kakaostore(url, output_dir):
    ################################################################################
    # 버튼 클릭안하고 실행하면 메인이미지랑 하단이미지 포함되고(버튼클릭전 이미 하나의div안에 있는듯)
    # 버튼 클릭하고 제대로 실행하면 대상컴퓨터에서 연결을 거부했다고 나옴
    # 결론은 버튼클릭안하고 모든이미지를 다받아와야됨
    ################################################################################
    print(f"kakaostore: {url}, {output_dir}")

    if not makedir(output_dir):
        return

    driver = initialize_and_open_url(url)
    if driver is None:
        return

    # kakaostore 상세보기버튼클릭
    # try:
    #     # 클래스명이 'btn_view'인 <a> 태그를 클릭하기 위해 대기
    #     detail_link = WebDriverWait(driver, 3).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn_view'))
    #     )
    #     detail_link.click()
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    # finally:
    #     driver.quit()
    # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    try:
        # 아니 상세부분 div 클래스명만 입력했는데 왜 메인이미지랑 하단에 쓰레기이미지까지 딸려오냐고
        kakaostore_class = ['.area_detail.ng-star-inserted']  # 아이디일땐 그냥 아이디값만
        # kakaostore_class = ['.contents.info_txt'] #버튼클릭할때 사용해야됨 아닐때는 위에것 사용
        # 대신 모든이미지 다나옴
        find_element_class(driver, kakaostore_class)
    except Exception as e:
        print(f"Error finding iframe: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        page_source = driver.page_source
        root = HTMLParser(page_source)
    except Exception as e:
        print(f"Error parsing page source: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        image_urls = []
        image_elements = root.css('img')
        for image_element in image_elements:
            image_urls.append(image_element.attributes['src'])
        print('get image_urls', image_urls)
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        traceback.print_exc()
        driver.quit()
        return

    try:
        save_images(image_urls, output_dir)
    except Exception as e:
        print(f"Error saving images: {e}")
        traceback.print_exc()

    print('kakaostore 완료중')
    driver.quit()


def oliveyoung(url, output_dir):
    print(f"oliveyoung: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    page_source = driver.page_source

    # 페이지 소스의 일부분 출력
    # print(page_source)

    # 주석으로 시작과 끝 찾기
    # 여기선 주석사용하니까 에러나면 주석 어디있나 찾아서 교체하면됨
    start_comment = "<!--상품상세시작-->"
    end_comment = "<!--상품상세시작 끝1-->"

    start_idx = page_source.find(start_comment)
    end_idx = page_source.find(end_comment)

    if start_idx == -1 or end_idx == -1:
        print("주석을 찾을 수 없습니다.")
        return

    # 주석 사이의 HTML 추출
    detail_html = page_source[start_idx + len(start_comment):end_idx]
    detail_parser = HTMLParser(detail_html)

    # 이미지 URL 추출
    image_urls = []
    image_elements = detail_parser.css('img')
    for image_element in image_elements:
        if 'src' in image_element.attributes:
            src = image_element.attributes['src']
            if not src.startswith('h'):
                data_src = image_element.attributes['data-src']
                image_urls.append(data_src)
            else:
                image_urls.append(src)

    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('oliveyoung 완료중')
    driver.quit()


def lotteimall(url, output_dir):
    ##########################################################
    # 중요한 상세이미지가 base64로 넘어오는데 이게 전체데이터가 아니라 앞대가리만 있는
    # 제시용 데이터라 디코딩시에 귀퉁이 작은이미지만 복원됨
    # rpa사용해야할듯
    print(f"lotteimall: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    page_source = driver.page_source
    # print(page_source)
    start_comment = "<!--//191115 해외직배송 안내사항 -->"
    end_comment = "<!-- The cache server responded. -->"

    start_idx = page_source.find(start_comment)
    end_idx = page_source.find(end_comment)

    if start_idx == -1 or end_idx == -1:
        print("주석을 찾을 수 없습니다.")
        return

    detail_html = page_source[start_idx + len(start_comment):end_idx]
    detail_parser = HTMLParser(detail_html)

    image_urls = []
    image_elements = detail_parser.css('img')

    for image_element in image_elements:
        image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)

    for i, image_url in enumerate(image_urls):
        try:
            if image_url.startswith('data:image/'):
                # Base64 이미지 처리
                header, encoded = image_url.split(",", 1)
                data = base64.b64decode(encoded)
                file_extension = header.split('/')[1].split(';')[0]
                file_name = f"image_{i}.{file_extension}"
                file_path = os.path.join(title_dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(data)
            else:
                # 일반 URL 이미지 처리
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                response = requests.get(image_url, headers=headers, stream=True)
                response.raise_for_status()
                file_extension = image_url.split('.')[-1]
                file_name = f"image_{i}.{file_extension}"
                file_path = os.path.join(title_dir, file_name)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except Exception as e:
            print(f"Error saving image {image_url}: {e}")

    print('lotteimall 완료중')
    driver.quit()


def ktalphashopping(url, output_dir):
    print(f"ktalphashopping: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    kt_class = ['.pd_info']  # 아이디일땐 그냥 아이디값만
    find_element_class(driver, kt_class)
    page_source = driver.page_source
    root = HTMLParser(page_source)

    image_urls = []
    image_elements = root.css('img')

    for image_element in image_elements:
        if 'src' in image_element.attributes:
            src = image_element.attributes['src']
            if src.startswith('https://shfile.'):
                image_urls.append(src)  # 어거지로 저렇게 시작하는 메인이미지만 담음/ 저걸로시작하지않으면 찌꺼지이미지

    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('ktalphashopping 완료중')
    driver.quit()


def skstore(url, output_dir):
    print(f"skstore: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    # sk_class = ['.pic1_info_detail'] #아이디일땐 그냥 아이디값만
    # find_element_class(driver, sk_class)
    page_source = driver.page_source
    # root = HTMLParser(page_source)
    start_comment = "<!--상품상세시작-->"
    end_comment = "<!--상품상세시작 끝1-->"
    start_idx = page_source.find(start_comment)
    end_idx = page_source.find(end_comment)
    if start_idx == -1 or end_idx == -1:
        print("주석을 찾을 수 없습니다.")
        return

    detail_html = page_source[start_idx + len(start_comment):end_idx]
    detail_parser = HTMLParser(detail_html)

    # 이미지 URL 추출
    image_urls = []
    image_elements = detail_parser.css('img')
    for image_element in image_elements:
        image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('skstore 완료중')
    driver.quit()


def ssglive(url, output_dir):
    print(f"ssglive: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    ssglive_class = ['#contentsTextQs']
    find_element_class(driver, ssglive_class)

    page_source = driver.page_source
    root = HTMLParser(page_source)

    # 이미지 URL 추출
    image_urls = []
    image_elements = root.css('img')

    exclude_classes = {'_image', 'qrcode', 'image', 'gtm_banner'}  # 필요없는 이미지 태그명

    for image_element in image_elements:
        image_classes = set(image_element.attributes.get('class', '').split())
        if not image_classes.intersection(exclude_classes):
            image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('ssglive 완료중')
    driver.quit()


def costcoonlinemall(url, output_dir):
    print(f"costcoonlinemall: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    images = driver.find_elements(By.CLASS_NAME, 'ng-star-inserted')
    src_list = [img.get_attribute('src') for img in images if img.get_attribute('src')]

    image_urls = []
    for rr in src_list:
        image_url = rr if rr.startswith('http') else 'https://www.costco.co.kr' + rr
        image_urls.append(image_url)

    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('costcoonlinemall 완료중')
    driver.quit()


def alieexpress(url, output_dir):
    print(f"alieexpress: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # 알리 상세보기버튼클릭
    detail_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.comet-v2-btn.comet-v2-btn-slim.comet-v2-btn-large.extend--btn--aAOvo5q.comet-v2-btn-important'))
    )
    detail_button.click()

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    # alie_class = ['.description--origin-part--SsZJoGc'] #아이디일땐 그냥 아이디값만
    alie_class = ['.extend--iframe--ZW0B1OE']
    find_element_class(driver, alie_class)
    page_source = driver.page_source
    root = HTMLParser(page_source)
    print(root.text())

    image_urls = []
    image_elements = root.css('img')
    for image_element in image_elements:
        image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('alieexpress 완료중')
    driver.quit()


def martbaemin(url, output_dir):  # 우아한형제들아님 배민상회임
    print(f"martbaemin: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    martbaemin_class = ['.sc-jShKGg.bmzpKK']

    find_element_class(driver, martbaemin_class)
    page_source = driver.page_source
    parser = etree.HTMLParser()
    tree = etree.fromstring(page_source, parser)

    # 배민은 다르게파싱해야함
    image_urls = []
    image_elements = tree.xpath('//img')
    for image_element in image_elements:
        src = image_element.get('src')  # get 메서드를 사용하여 src 속성을 가져옴
        if src:
            image_urls.append(src)

    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('martbaemin 완료중')
    driver.quit()


def gsshop(url, output_dir):  # 우아한형제들아님 배민상회임
    print(f"gsshop: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    gsshop_class = 'prdDetailIfr'

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, gsshop_class))
    )
    driver.switch_to.frame(element)

    page_source = driver.page_source
    root = HTMLParser(page_source)

    # 배민은 다르게 파싱해야함
    image_urls = []
    image_elements = root.css('img')
    for image_element in image_elements:
        image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('gsshop 완료중')
    driver.quit()


def image_crawling(info):
    if len(info) != 3:
        print("Error: 필수 파라미터를 확인하세요")
        return

    # AA에서 파라미터 리스트로넘겨줌
    commerce_code = info[0]  # 첫 번째 파라미터: 커머스코드
    img_url = info[1]  # 두 번째 파라미터: 이미지url
    save_path = info[2]  # 세 번째 파라미터: 저장장소

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

    if commerce_code == 'naver_brand':
        naver_brand(img_url, save_path)

    if commerce_code == 'naver_shopping':
        naver_search_shopping(img_url, save_path)

    if commerce_code == 'ssg':
        ssg(img_url, save_path)

    if commerce_code == 'cjthemarket':
        cjthemarket(img_url, save_path)

    if commerce_code == 'hmall':
        hmall(img_url, save_path)

    if commerce_code == 'lotteon':
        lotteon(img_url, save_path)

    if commerce_code == 'cjonstyle':
        cjonstyle(img_url, save_path)

    if commerce_code == 'emartmall':
        emartmall(img_url, save_path)

    if commerce_code == 'kakaostore':
        kakaostore(img_url, save_path)

    if commerce_code == 'oliveyoung':
        oliveyoung(img_url, save_path)

    if commerce_code == 'lotteimall':  # ==lottehomeshopping 둘이 같은듯, 네이버스마트스토어의 롯데홈쇼핑이면 네이버로 사용하면됨
        lotteimall(img_url, save_path)

    if commerce_code == 'ktalphashopping':
        ktalphashopping(img_url, save_path)

    if commerce_code == 'skstore':
        skstore(img_url, save_path)

    if commerce_code == 'ssglive':
        ssglive(img_url, save_path)  # 그냥신세계몰과 신세계라이브쇼핑하고 다르다 #참고로 기존에 신세계쇼핑이라고 써져있는데 신세계라이브쇼핑이다

    if commerce_code == 'costcoonlinemall':
        costcoonlinemall(img_url, save_path)

    if commerce_code == 'alieexpress':
        alieexpress(img_url, save_path)

    if commerce_code == 'martbaemin':
        martbaemin(img_url, save_path)

    if commerce_code == 'gsshop':
        gsshop(img_url, save_path)


# 로컬에서 실행test
if __name__ == "__main__":
    ####################
    # a = 'ssg'
    # # b = 'https://www.ssg.com/item/itemView.ssg?itemId=1000305886979&siteNo=6004&salestrNo=6005&tlidSrchWd=CJ%20%ED%96%87%EB%B0%98&srchPgNo=1&src_area=ssglist'
    # b = 'https://www.ssg.com/item/itemView.ssg?itemId=1000305886979&siteNo=6004&salestrNo=6005&tlidSrchWd=CJ%20%ED%96%87%EB%B0%98&srchPgNo=1&src_area=ssglist'
    # c = "C:/Users/Rainbow Brain/Desktop/test/ssg"
    ##########################################
    # a = 'elevenst'
    # b = 'https://www.11st.co.kr/products/5395841477?&trTypeCd=PW24&trCtgrNo=585021'
    # c = "C:/Users/Rainbow Brain/Desktop/test/elevenst"
    ##########################################
    # a = 'auction'
    # b = 'http://itempage3.auction.co.kr/DetailView.aspx?itemno=C499114079'
    # c = "C:/Users/Rainbow Brain/Desktop/test/auction"
    ##########################################
    # a = sys.argv[0]
    # b = sys.argv[1]
    # c = sys.argv[2]
    ##########################################
    # a = 'gmarket'
    # b = 'https://item.gmarket.co.kr/Item?goodscode=3499614468&buyboxtype=ad'
    # c = "C:/Users/Rainbow Brain/Desktop/test/gmarket"
    ##########################################
    # a = 'cjthemarket'
    # b = 'https://www.cjthemarket.com/pc/prod/prodDetail?prdCd=40183168&plnId=300004&areaNum=74'
    # c = "C:/Users/Rainbow Brain/Desktop/test/cjthemarket"
    ##########################################
    # 네이버는 뭘써야되는거냐 brand / search.shopping
    # a = 'naver_brand'
    # b = 'https://brand.naver.com/cheiljedang/products/6042668419' #햇반 됨
    # c = "C:/Users/Rainbow Brain/Desktop/test/naver_brand"
    # a = 'naver_shopping'
    # b = 'https://search.shopping.naver.com/catalog/5679111748'  # 다시다 안됨
    # c = "C:/Users/Rainbow Brain/Desktop/test/naver_shopping"
    ##########################################
    # a = 'HmaLL'
    # b = 'https://www.hmall.com/pd/pda/itemPtc?slitmCd=2212437659&searchTerm=cj'
    # c = "C:/Users/Rainbow Brain/Desktop/test/hmall"
    ##########################################
    # a = 'lotteon'
    # b = 'https://www.lotteon.com/p/product/LO2067278567'
    # c = "C:/Users/Rainbow Brain/Desktop/test/lotteon"
    ##########################################
    # a = 'cjonstyle'
    # b = 'https://display.cjonstyle.com/p/item/2014282135'
    # c = "C:/Users/Rainbow Brain/Desktop/test/cjonstyle"
    ##########################################
    # a = 'eMartMall'
    # b = 'https://emart.ssg.com/item/itemView.ssg?itemId=1000571764822'
    # c = "C:/Users/Rainbow Brain/Desktop/test/emartmall"
    ##########################################
    # a = 'kakaostore'
    # # b = 'https://store.kakao.com/cheiljedang/products/218641145'
    # b = 'https://store.kakao.com/cheiljedang/products/149592517?docId=149592517'
    # c = "C:/Users/Rainbow Brain/Desktop/test/kakaostore"
    ##########################################
    a = 'oliveyoung'
    b = 'https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=B000000184481'
    c = "C:/Users/Rainbow Brain/Desktop/test/oliveyoung"
    ##########################################
    # a = 'lotteimall'
    # b = 'https://www.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no=2512242592'
    # c = "C:/Users/Rainbow Brain/Desktop/test/lotteimall"
    ##########################################
    # a = 'ktalphashopping'
    # b = 'https://www.kshop.co.kr/display/ec/product/2751563?srwrVal=cj'
    # c = "C:/Users/Rainbow Brain/Desktop/test/ktalphashopping"
    ##########################################
    # a = 'skstore'
    # b = 'https://www.skstoa.com/display/goods/27843605'
    # c = "C:/Users/Rainbow Brain/Desktop/test/skstore"
    ##########################################
    # a = 'ssglive'
    # b = 'https://www.shinsegaetvshopping.com/display/detail/20056722'
    # c = "C:/Users/Rainbow Brain/Desktop/test/ssglive"
    ##########################################
    # a = 'costcoonlinemall'
    # b = 'https://www.costco.co.kr/Foods/Chilled-Foods/Chilled-Foods/CJ-Mijungdang-Soup-Style-Tteokbokki-4012g-x-8ea/p/662498'
    # c = "C:/Users/Rainbow Brain/Desktop/test/costcoonlinemall"
    ##########################################
    # a = 'alieexpress'
    # b = 'https://ko.aliexpress.com/item/1005006562460420.html?spm=a2g0o.productlist.main.3.2ea53l6p3l6pN1&algo_pvid=5e733517-e786-4d12-9ff5-8fc1053711e9&algo_exp_id=5e733517-e786-4d12-9ff5-8fc1053711e9-1&pdp_npi=4%40dis%21KRW%2142320%2117774%21%21%2142320%2117774%21%402140d2dc17210930602674403e8a73%2112000037680917513%21sea%21KR%210%21AB&curPageLogUid=yHsq6pRu1o4j&utparam-url=scene%3Asearch%7Cquery_from%3A'
    # c = "C:/Users/Rainbow Brain/Desktop/test/alie"
    ##########################################
    # a = 'martbaemin' #배민상회
    # b = 'https://mart.baemin.com/goods/detail/217341'
    # c = "C:/Users/Rainbow Brain/Desktop/test/martbaemin"
    ##########################################
    # a = 'gsshop'
    # b = 'https://www.gsshop.com/prd/prd.gs?prdid=56335104'
    # c = "C:/Users/Rainbow Brain/Desktop/test/gsshop"
    ##########################################

    param = [a, b, c]

    image_crawling(param)

# python onefile/imgclusterandcompare.py ssg "https://www.11st.co.kr/products/5395841477?&trTypeCd=PW24&trCtgrNo=585021" "C:/Users/Rainbow Brain/Desktop/elevenImages"
# python onefile/imgclusterandcompare.py
