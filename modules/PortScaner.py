import socket
ip = input("目标主机:")
timeout = float(input("超时："))
ports = []
print("开始检测...")
for i in range(0,65536):
    a = socket.socket()
    a.settimeout(timeout)
    try:
        print(i, end = "\r")
        a.connect((ip, i))
        ports.append(i)
        print("侦测到端口:",i)
        #a.close()
        del a
    except Exception:
        pass
print(ip, "开放的端口:", ports, "个数:", len(ports))
