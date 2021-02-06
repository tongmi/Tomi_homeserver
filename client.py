#!/bin/python3
import socket as s
try:
    c=s.socket()
except:
    print("未知错误.\nUnkown error.")
    exit()
try:
    c.connect(("tongmios.iask.in",30577))
except:
    print("服务器离线。\nThe server is offline.")
    c.close()
    exit()
str0=c.recv(1024).decode("utf-8")
print(str0)
c.close()

