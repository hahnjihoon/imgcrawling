import shlex

import requests
import os
import sys
import tempfile
import subprocess
import base64
import time
import json

# python testete.py Japan

if len(sys.argv) != 2:
    print("Enter one country at a time!")
    exit(1)
cntry = sys.argv[1]

if len(cntry) > 2:
    j = 5
elif len(cntry) == 2:
    j = 6
else:
    print("Cannot identify the country. Name is too short.")
    exit(1)

try:
    vpnServerListData = requests.get("http://www.vpngate.net/api/iphone/").text.replace(
        "\r", ""
    )
    freeServers = [line.split(",") for line in vpnServerListData.split("\n")]
    serverLabels = freeServers[1]
    serverLabels[0] = serverLabels[0][1:]
    freeServers = [srvrs for srvrs in freeServers[2:] if len(srvrs) > 1]
except:
    print("Something is wrong! Cannot load the VPN server's data")
    exit(1)

availableServers = [
    srvrs for srvrs in freeServers if cntry.lower() in srvrs[j].lower()
]
numOfServers = len(availableServers)
print("We found " + str(numOfServers) + " servers for " + cntry)
if numOfServers == 0:
    exit(1)

supporteServers = [srvrs for srvrs in availableServers if len(srvrs[-1]) > 0]
print(str(len(supporteServers)) + " of these servers support OpenVPN")

bestServer = sorted(
    supporteServers,
    key=lambda srvrs: float(srvrs[2].replace(",", ".")),
    reverse=True,
)[0]
print("\n== Best server ==")
labelPair = list(zip(serverLabels, bestServer))[:-1]
for (l, d) in labelPair[:4]:
    print(l + ": " + d)
print(labelPair[4][0] + ": " + str(float(labelPair[4][1]) / 10 ** 6) + " MBps")
print("Country: " + labelPair[5][1])

print('tlqkftlqkwer')
# _, path = tempfile.mkstemp(suffix='.ovpn')
# file = open(path, "wb")
# file.write(base64.b64decode(bestServer[-1]))
# file.close()
# vpnR = subprocess.Popen(["openvpn", "--config", path])

conf_path = r"C:\Users\Rainbow Brain\Downloads\vpngate_vpn200125347.opengw.net_udp_1195.ovpn"
vpn_process = subprocess.Popen(["openvpn", "--config", conf_path])
print('VPN이 실행됨')
vpnR = subprocess.Popen(["openvpn", "--config", vpn_process])

# cmd = 'start /b cmd /c "C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --connect config.ovpn'
# args = shlex.split(cmd)
# x = subprocess.Popen(args, shell=True)
# print('xxxxxxxxxxxxxxx', x)

try:
    # time required to connect the openvpn to connect the vpn server
    time.sleep(10)

    # VPN이 실행된 후 외부 IP 주소 확인
    external_ip = requests.get("http://api.ipify.org").text
    print("External IP Address:", external_ip)

    # 여기에 쿠팡에 접속하여 HTML을 가져오는 코드를 추가하시면 됩니다.
    response = requests.get("https://www.coupang.com/")
    if response.status_code == 200:
        print("Successfully connected to Coupang")
        html_content = response.text
        print(html_content)
        # 여기서부터 원하는 작업을 수행하면 됩니다.
        # break
    else:
        print("Failed to connect to Coupang. Retrying...")
        time.sleep(5)  # 5초 후 다시 시도합니다.

except Exception as ex:
    print("An error occurred:", ex)

finally:
    vpnR.kill()
