#!/bin/python3
# -*- coding: UTF-8 -*-
import socket as s
try:
    c = s.socket()
except Exception:
    print("未知错误.\nUnkown error.")
    exit()
try:
    c.connect(("127.0.0.1", 31313))
except Exception:
    print("服务器离线。\nThe server is offline.")
    c.close()
    exit()
str0 = c.recv(1024).decode("utf-8")
print(str0)
c.close()

