import subprocess
import time
import requests

# OpenVPN 실행 파일 경로
openvpn_path = 'C:/Program Files/OpenVPN/bin/openvpn.exe'

# VPN 연결
def connect_vpn(config_path):
    vpn_process = subprocess.Popen(
        [openvpn_path, '--config', config_path],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True  # 텍스트 모드로 설정
    )
    time.sleep(10)  # VPN 연결 대기 시간 (필요에 따라 조정)
    return vpn_process

# VPN 연결 해제
def disconnect_vpn(vpn_process):
    vpn_process.terminate()
    vpn_process.wait()

# 현재 IP 주소 확인
def get_current_ip():
    try:
        response = requests.get('http://api.ipify.org?format=json')
        return response.json()['ip']
    except Exception as e:
        print(f"IP 주소를 가져오는 데 실패했습니다: {e}")
        return None

def main():
    vpn_config_path = 'C:/openvpn/vpnbook-us1-tcp443.ovpn'  # .ovpn 파일 경로

    # 1. VPN 연결
    vpn_process = connect_vpn(vpn_config_path)

    try:
        # VPN 연결 후 외부 IP 주소 확인
        current_ip = get_current_ip()
        print(f"현재 외부 IP 주소: {current_ip}")

        # VPN 연결 후 작업 수행
        # (예: 웹 크롤링, 데이터 다운로드 등)
        pass
    finally:
        # 3. VPN 연결 해제
        disconnect_vpn(vpn_process)
        print("VPN 연결 해제 완료")

if __name__ == "__main__":
    main()
