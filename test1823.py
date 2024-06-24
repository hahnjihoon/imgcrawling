from selenium import webdriver
import socket
import requests

print("외부ip :: ", requests.get("http://ip.jsontest.com").json()['ip'])

# print("내부ip :: ", socket.gethostbyname(socket.gethostname()))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("pwnbit.kr", 443))
print("내부ip :: ", sock.getsockname()[0])

def selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    dfadfasdf = webdriver.Chrome()



    return dfadfasdf


if __name__ == "__main__":
    url = 'https://www.whatismyip.com/'
    driver = selenium_driver()
    driver.get(url)
    # print("변경된 IP 주소:", driver.page_source.strip())
    # print(driver.page_source)
    input("Press Enter to quit...")
    driver.quit()