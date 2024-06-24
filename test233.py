import time
import subprocess
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# Tor를 시작하는 함수
# def start_tor():
#     asdfasdf = subprocess.Popen(['C:/Users/Rainbow Brain/Desktop/Tor Browser/Browser/firefox.exe'])
#     time.sleep(5)  # Tor가 시작될 시간을 줍니다
#     return asdfasdf
#
#
# # Tor에서 새로운 IP 주소를 받아오는 함수
# def get_new_ip():
#     with Controller.from_port(port=9051) as controller:
#         # controller.authenticate(password='YOUR_PASSWORD')  # torrc 파일에 설정한 패스워드를 입력합니다
#         controller.signal(Signal.NEWNYM)
#
#
# # Tor를 시작합니다
# tor_process = start_tor()
#
# # 새로운 IP 주소를 받아옵니다
# get_new_ip()
#
# # Firefox WebDriver 초기화
# driver = webdriver.Firefox()
#
# # 프록시 설정
# # driver.get('http://icanhazip.com/')
# driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.FIREFOX, browser_profile=profile)
#
# # 현재 페이지의 소스를 출력
# print(driver.page_source)
#
# # WebDriver 종료
# driver.quit()
#
# # Tor 프로세스를 종료합니다
# tor_process.terminate()


profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "127.0.0.1")
profile.set_preference("network.proxy.socks_port", 9050)

profile.update_preferences()

# driver = webdriver.Firefox(profile)
# driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.FIREFOX, browser_profile=profile)
driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX, browser_profile=profile)

driver.get('http://icanhazip.com/')

print(driver.page_source)

driver.quit()
