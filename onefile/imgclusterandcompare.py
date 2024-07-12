import os
from io import BytesIO
import requests
from PIL import Image
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def find_element_class(driver, selectors):
    loop_count = 0
    for selector in selectors:
        loop_count += 1
        print(f"Trying selector {loop_count}: {selector}")
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
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
    # 저장할 디렉토리가 존재하지 않으면 생성합니다.
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)

    for index, image_url in enumerate(image_urls):
        try:
            # 이미지 URL에서 이미지를 요청합니다.
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))

            # 이미지가 팔레트 모드(P)인지 확인하고, 그렇다면 RGB 모드로 변환합니다.
            # 팔레트모드가 gif이고 이건 보통 커머스에서올리는데 이거그냥 제끼고 다운받으면될듯
            if image.mode == 'P':
                image = image.convert('RGB')

            # 이미지 저장 경로를 생성합니다.
            image_path = os.path.join(title_dir, f'image_{index}.jpg')

            # 이미지를 JPEG 형식으로 저장합니다.
            image.save(image_path)
            print(f"Saved image: {image_path}")

        except Exception as e:
            # 예외가 발생할 경우 오류 메시지를 출력합니다.
            print(f"Error saving image {image_url}: {e}")


def auction(url, output_dir):
    print(f"auction: {url}, {output_dir}")
    print('auction fine :: ', url)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # 옥션에만있는 상세보기버튼클릭
    detail_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.js-toggle-button'))
    )
    detail_button.click()

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    # 실제 iframe안에 상태 이미지가 있으므로
    # iframe_element = driver.find_element(By.ID, "hIfrmExplainView")
    # driver.switch_to.frame(iframe_element)  # iframe 내부로 전환
    auction_class = ['.11test', '.testest', 'hIfrmExplainView']
    find_element_id(driver, auction_class)

    page_source = driver.page_source
    root = HTMLParser(page_source)

    image_urls = []
    image_elements = root.css('#hdivDescription img')
    for image_element in image_elements:
        image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
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

    # 실제 iframe안에 상태 이미지가 있으므로 iframe으로 전환
    # iframe_element = WebDriverWait(driver, 3).until(
    #     EC.presence_of_element_located((By.ID, "prdDescIfrm"))
    # )
    # driver.switch_to.frame(iframe_element)
    eleven_class = ['.11test', '.3dkeje', 'prdDescIfrm']
    find_element_id(driver, eleven_class)

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
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
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

    gmarket_class = ['.ddd', 'test', 'detail1']
    find_element_id(driver, gmarket_class)

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
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

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
    print(f"naver: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    # options.add_argument('--headless') #네이버는 화면을 켜야됨 = rpa가 하는게 나음
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-webgl')
    driver = webdriver.Chrome(options=options)

    # naver_login(driver)

    driver.get(url)

    # cookies = driver.get_cookies()
    # print("Session cookies:::::::::::::::::::::::::::::::::::::::")
    # for cookie in cookies:
    #     print(cookie)

    print('버튼클릭전') #화면자체를 켜서 눌러야됨 코드상으로는 api를 호출해서 검증하는듯 그래서 안됨
    button_xpath = '//*[@id="INTRODUCE"]/div/div[5]/button'
    button_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, button_xpath))
    )
    button_element.click()
    time.sleep(2)

    print('버튼 클릭 성공')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
    )

    page_source = driver.page_source
    root = HTMLParser(page_source)

    #이미지파싱도 일부분은 javascript를 사용해서 구현하는듯, 그래서 https가 아닌 이미지url이 나옴 = 그런건 저장안됨
    image_urls = []
    image_elements = root.css(
        '#INTRODUCE > div > div._3osy73V_eD._1Hc_ju_IXp._2pWm5xPRcr > div:nth-child(1) > div:nth-child(2) > div._9F9CWn02VE > div > div > div > div img')

    #원래꺼
    # for image_element in image_elements:
    #     if 'src' in image_element.attributes:
    #         src = image_element.attributes['src']
    #         image_urls.append(src)

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

    print('naver 완료중')
    driver.quit()

def naver_search_shopping(url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    # options.add_argument('--headless') #네이버는 화면을 켜야됨 = rpa가 하는게 나음
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-webgl')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # title_div = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.top_summary_title__ViyrM'))
    # )
    #
    # # title_div 내부의 h2 태그를 찾음
    # h2_element = title_div.find_element(By.TAG_NAME, 'h2')
    #
    # # h2 요소의 텍스트 추출
    # h2_text = h2_element.text
    # print(h2_text)

    # 막힌듯
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#container'))
    )
    page_source = driver.page_source
    root = HTMLParser(page_source)
    print('root:: ', root.text())

    image_urls = []
    image_elements = root.css(
        'div.additionalImages_product_img__ALP0s img')
    print('ddddddddddddddddddddddddddddd', image_elements)

    for image_element in image_elements:
        if 'src' in image_element.attributes:
            image_urls.append(image_element.attributes['src'])
    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('naver_search 완료중')
    driver.quit()

def ssg(url, output_dir):
    print('ssg시작')
    print(f"ssg: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # ssg에만있는 상세보기버튼클릭
    detail_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.ctrl_collapse'))
    )
    detail_button.click()

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

    # 실제 iframe안에 상태 이미지가 있으므로
    # iframe_element = driver.find_element(By.ID, "_ifr_html")
    # driver.switch_to.frame(iframe_element)  # iframe 내부로 전환
    ssg_class = ['aaaaa', '.product-tail2', '_ifr_html']
    find_element_id(driver, ssg_class)
    page_source = driver.page_source
    root = HTMLParser(page_source)

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

    print('ssg 완료중')
    driver.quit()


def cjthemarket(url, output_dir):
    print(f"cjthemarket: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # cj the market은 상세보기버튼없이 펼쳐져있음
    # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-detail')))
    # # print('detail :: ', detail)
    # driver.find_element(By.CSS_SELECTOR, ".product-detail")
    cjthemarket_class = ['aaaaa', '.product-tail2', '.product-detail']
    find_element_class(driver, cjthemarket_class)

    page_source = driver.page_source
    root = HTMLParser(page_source)
    print(root.text())

    image_urls = []

    # div 클래스명프로덕트디테일하위의 img다 찾으란소리 이거말고 아예 필요이미지만 있는 상위 div클래스명 필요
    # 찾기힘들면 xpath 복사하면됨
    image_elements = root.css(
        '#prdDetail > div.product-detail-images.mt40.slick-initialized.slick-slider.slick-dotted > div.slick-list > div > div:nth-child(3) img')

    # cjthemarket은 src에 http:가 쳐 빠져있음 붙여서 리스트업
    for image_element in image_elements:
        # src 속성을 가져와서 앞에 http: 붙이기
        url = 'http:' + image_element.attributes['src']
        image_urls.append(url)

    print('get image_urls', image_urls)

    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('cj the market 완료중')
    driver.quit()

def hmall(url, output_dir):
    print(f"hmall: {url}, {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    hmall_class = ['.view-content']
    find_element_class(driver, hmall_class)

    #아니 hmall은 파싱하면 html이 안나오고 이상한게 나오도록 한듯
    page_source = driver.page_source
    root = HTMLParser(page_source)
    # print(root.text())

    image_urls = []
    image_elements = root.css(
        '.view-content img')

    for image_element in image_elements:
        image_urls.append(image_element.attributes['src'])

    print('get image_urls', image_urls)

    # 이미지 저장
    title_dir = os.path.join(output_dir)
    if not os.path.exists(title_dir):
        os.makedirs(title_dir)
    save_images(image_urls, title_dir)

    print('ssg 완료중')
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

    if commerce_code == 'naver':
        # naver_brand(img_url, save_path)
        naver_search_shopping(img_url, save_path)

    if commerce_code == 'ssg':
        ssg(img_url, save_path)

    if commerce_code == 'cjthemarket':
        cjthemarket(img_url, save_path)

    if commerce_code == 'hmall':
        hmall(img_url, save_path)


# 로컬에서 실행test
if __name__ == "__main__":
    ####################
    # a = 'ssg'
    # # b = 'https://www.ssg.com/item/itemView.ssg?itemId=1000305886979&siteNo=6004&salestrNo=6005&tlidSrchWd=CJ%20%ED%96%87%EB%B0%98&srchPgNo=1&src_area=ssglist'
    # b = 'https://www.ssg.com/item/itemView.ssg?itemId=1000575565793'
    # c = "C:/Users/Rainbow Brain/Desktop/save"
    ##########################################
    # a = 'elevenst'
    # b = 'https://www.11st.co.kr/products/5395841477?&trTypeCd=PW24&trCtgrNo=585021'
    # c = "C:/Users/Rainbow Brain/Desktop/elevenImages"
    ##########################################
    # a = 'auction'
    # b = 'http://itempage3.auction.co.kr/DetailView.aspx?itemno=C499114079'
    # c = "C:/Users/Rainbow Brain/Desktop/auctionImgaes"
    ##########################################
    # a = sys.argv[0]
    # b = sys.argv[1]
    # c = sys.argv[2]
    ##########################################
    # a = 'gmarket'
    # b = 'https://item.gmarket.co.kr/Item?goodscode=3499614468&buyboxtype=ad'
    # c = "C:/Users/Rainbow Brain/Desktop/save"
    ##########################################
    # a = 'cjthemarket'
    # b = 'https://www.cjthemarket.com/pc/prod/prodDetail?prdCd=40183168&plnId=300004&areaNum=74'
    # c = "C:/Users/Rainbow Brain/Desktop/save"
    ##########################################
    # 네이버는 뭘써야되는거냐 brand / search.shopping
    # a = 'naver'
    # # b = 'https://brand.naver.com/cheiljedang/products/6042668419' #햇반 됨
    # b = 'https://search.shopping.naver.com/catalog/5679111748' #다시다 안됨
    # c = "C:/Users/Rainbow Brain/Desktop/save"
    ##########################################
    a = 'HmaLL'
    b = 'https://www.hmall.com/pd/pda/itemPtc?slitmCd=2212437659&searchTerm=cj'
    c = "C:/Users/Rainbow Brain/Desktop/hmallsave"

    param = [a, b, c]

    image_crawling(param)

# python onefile/imgclusterandcompare.py ssg "https://www.11st.co.kr/products/5395841477?&trTypeCd=PW24&trCtgrNo=585021" "C:/Users/Rainbow Brain/Desktop/elevenImages"
# python onefile/imgclusterandcompare.py
