from typing import List, Iterable
import datetime
import re

from selectolax.parser import HTMLParser
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

import random
import aiohttp
import time
from bs4 import BeautifulSoup

import requests

from stem import Signal
from stem.control import Controller

from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.request import urlopen

from selenium import webdriver

import subprocess


def start_tor():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='YOUR_PASSWORD')  # 'YOUR_PASSWORD'를 실제 Tor 비밀번호로 변경
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())


# Tor 프로세스를 시작하는 함수
def setup_tor():
    process = subprocess.Popen(['tor', '-f', 'c:/users/rainbow brain/appdata/localp/rograms/python/python310/lib/site-packages'])  # 경로를 시스템에 맞게 조정
    time.sleep(5)  # Tor가 시작될 시간을 줍니다
    return process

PORT = 9097

tor_subprocess = setup_tor()  # 변수 이름 변경

driver = ''

try:
    start_tor()

    # 프록시 설정
    proxy_ip_port = "127.0.0.1:9050"
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'socksProxy': proxy_ip_port,
        'socksVersion': 5,
    })

    # Firefox 옵션 생성 및 프록시 설정 추가
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.proxy = proxy
    firefox_options.set_preference('network.proxy.type', 1)
    firefox_options.set_preference('network.proxy.socks', '127.0.0.1')
    firefox_options.set_preference('network.proxy.socks_port', 9050)
    firefox_options.set_preference('network.proxy.socks_remote_dns', True)  # DNS 요청도 프록시를 통해 보냅니다
    firefox_options.headless = True  # 필요에 따라 헤드리스 모드 사용

    # WebDriver 초기화
    driver = webdriver.Firefox(options=firefox_options)

    # IP 주소 확인
    driver.get('http://icanhazip.com/')
    print("변경된 IP 주소:", driver.page_source.strip())

    input("Press Enter to quit...")

finally:
    if driver:
        driver.quit()
    tor_subprocess.terminate()  # 변수 이름 변경
