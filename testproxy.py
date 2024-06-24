from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from selectolax.parser import HTMLParser


def get_proxy_list():
    global pct
    url = 'http://spys.one/en/free-proxy-list/'
    data = {"xpp": "1", "xf1": "0", "xf2": "0", "xf4": "0", "xf5": "2"}
    r = requests.post(url, data=data)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Result list of IP and Port
    result = []

    # Get pre-defined number combination
    ports = {}
    script = soup.select_one("body > script")
    # print(script)
    for row in script.text.split(";"):
        if "^" in row:
            line = row.split("=")
            ports[line[0]] = line[1].split("^")[0]

    # Each rows
    trs = soup.select("tr[onmouseover]")
    print(trs)
    for tr in trs:
        e_ip = tr.select_one("font.spy14")
        ip = ""

        # Get port number
        e_port = tr.select_one("script")
        port = ""
        if e_port is not None:
            re_port = re.compile(r'\(([a-zA-Z0-9]+)\^[a-zA-Z0-9]+\)')
            match = re_port.findall(e_port.text)
            for item in match:
                port = port + ports[item]
        else:
            continue

        # Get ip number
        if e_ip is not None:
            for item in e_ip.findAll('script'):
                item.extract()
            ip = e_ip.text
        else:
            continue

        # Get uptime value (%)
        tds = tr.select("td")
        is_skip = False
        for td in tds:
            e_pct = td.select_one("font > acronym")
            if e_pct is not None:
                pct = re.sub('([0-9]+)%.*', r'\1', e_pct.text)
                if not pct.isdigit():
                    is_skip = True
            else:
                continue
        if is_skip:
            continue

        result.append((ip + ":" + port, pct))

    # Sort by uptime value
    result.sort(key=lambda element: int(element[1]), reverse=True)

    return result


if __name__ == "__main__":
    # proxy_list = get_proxy_list()
    # print(proxy_list)
    var = [('211.33.121.143:1080', '100'), ('202.69.59.29:1080', '100'), ('194.1.239.184:1080', '100'),
           ('186.127.10.244:1080', '100'), ('186.127.1.66:1080', '100'), ('186.126.245.98:1080', '100'),
           ('185.229.109.132:1080', '100'), ('185.161.211.25:1080', '100'), ('181.7.198.88:1080', '100'),
           ('181.3.57.107:1080', '100'), ('181.3.156.101:1080', '100'), ('181.106.239.33:1080', '100'),
           ('181.102.86.36:1080', '100'), ('181.102.79.149:1080', '100'), ('181.102.53.37:1080', '100'),
           ('181.102.200.107:1080', '100'), ('181.3.25.217:1080', '78'), ('222.165.225.245:3468', '77'),
           ('217.61.130.19:3341', '76'), ('181.5.207.9:1080', '75'), ('181.3.87.72:1080', '75'),
           ('181.102.31.147:1080', '75'), ('186.127.16.94:1080', '67'), ('181.5.245.47:1080', '67'),
           ('181.3.17.228:1080', '67'), ('181.82.237.248:1080', '64'), ('212.83.191.157:8128', '63'),
           ('182.93.84.130:62633', '62'), ('181.102.56.187:1080', '57'), ('181.82.235.116:1080', '56'),
           ('181.5.193.146:1080', '54'), ('181.82.239.204:1080', '51'), ('186.127.244.72:1080', '50'),
           ('186.127.19.82:1080', '50'), ('181.5.201.2:1080', '50'), ('181.3.1.12:1080', '50'), ('181.102.57.141:1080',
                                                                                                 '50'),
           ('217.182.230.15:4485', '43'), ('181.5.242.86:1080', '38'), ('185.180.40.70:9050', '29')]
    # 211.33.121.143:1080
    # print(var[0][0])

    proxy_list = var

    for i in range(4):
        proxy = {'http': f'socks5://{proxy_list[1][0]}'}
        print(proxy)
        try:
            response = requests.get('https://www.coupang.com/vp/products/328677319?itemId=1051091399', proxies=proxy, timeout=5)
            print(f"Proxy Success: {proxy_list[0]} - Status Code: {response.status_code}")
            print(response.text)
            root = HTMLParser(response.text)
            print(root)
            break  # 성공적으로 응답을 받았을 때 루프를 종료합니다.
        except Exception as e:
            print(f"Proxy Error for {proxy_list[0]}: {e}")
