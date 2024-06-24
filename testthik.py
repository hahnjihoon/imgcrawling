import tkinter as tk
from tkinter import messagebox
import wmi

# WMI 객체 생성
wmi_obj = wmi.WMI()

# 네트워크 어댑터를 가져와서 리스트에 저장
adapter_config = wmi_obj.Win32_NetworkAdapterConfiguration(IPEnabled=True)
adapter_list = [adapter.Caption for adapter in adapter_config]

# tkinter GUI 생성
root = tk.Tk()
root.title("네트워크 설정 변경")

# 어댑터 선택 프레임
adapter_frame = tk.Frame(root)
adapter_label = tk.Label(adapter_frame, text="어댑터 선택:")
adapter_label.grid(padx=5, pady=5)
adapter_var = tk.StringVar()
adapter_var.set(adapter_list[0])
adapter_menu = tk.OptionMenu(adapter_frame, adapter_var, *adapter_list)
adapter_menu.grid(padx=5, pady=5)
adapter_frame.pack()

# IP, 서브넷 마스크, 게이트웨이, DNS 서버 주소 입력 프레임
ip_frame = tk.Frame(root)
ip_label = tk.Label(ip_frame, text="IP 주소:")
ip_label.grid(padx=5, pady=5)
ip_entry = tk.Entry(ip_frame)
ip_entry.grid(padx=5, pady=5)
ip_frame.pack()

subnet_mask_frame = tk.Frame(root)
subnet_mask_label = tk.Label(subnet_mask_frame, text="서브넷 마스크:")
subnet_mask_label.grid(padx=5, pady=5)
subnet_mask_entry = tk.Entry(subnet_mask_frame)
subnet_mask_entry.grid(padx=5, pady=5)
subnet_mask_frame.pack()

gateway_frame = tk.Frame(root)
gateway_label = tk.Label(gateway_frame, text="게이트웨이:")
gateway_label.grid(padx=5, pady=5)
gateway_entry = tk.Entry(gateway_frame)
gateway_entry.grid(padx=5, pady=5)
gateway_frame.pack()

dns_frame = tk.Frame(root)
dns_label = tk.Label(dns_frame, text="DNS 서버 주소:")
dns_label.grid(padx=5, pady=5)
dns_entry1 = tk.Entry(dns_frame)
dns_entry1.grid(padx=5, pady=5)
dns_frame.pack()

dns_frame1 = tk.Frame(root)
dns_label2 = tk.Label(dns_frame1, text="보조 DNS 서버 주소:")
dns_label2.grid(padx=5, pady=5)
dns_entry2 = tk.Entry(dns_frame1)
dns_entry2.grid(padx=5, pady=5)
dns_frame1.pack()

# 변경 버튼
def change_settings():
    selected_adapter = adapter_var.get()
    ip_address = ip_entry.get().split(",")
    subnet_mask = subnet_mask_entry.get().split(",")
    gateway = gateway_entry.get().split(",")
    dns_server = [dns_entry1.get(), dns_entry2.get()]
    for adapter in adapter_config:
        if adapter.Caption == selected_adapter:
            adapter.EnableStatic(IPAddress=ip_address, SubnetMask=subnet_mask)
            adapter.SetGateways(DefaultIPGateway=gateway)
            adapter.SetDNSServerSearchOrder(DNSServerSearchOrder=dns_server)
            messagebox.showinfo("Error","설정이 변경되었습니다.")
            break

change_button = tk.Button(root, text="변경", command=change_settings)
change_button.pack()

# 결과 텍스트
result_label = tk.Label(root)
result_label.pack()

root.mainloop()