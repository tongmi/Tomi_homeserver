#!/bin/python3
# -*- coding: UTF-8 -*-
import socket as s
from _thread import start_new_thread as t
c=s.socket()
hostname=input("Hostname:")
while True:
    try:
        port=int(input("Port:"))
        break
    except:
        print("It is not a port!Please type again.")
c.settimeout(30.0)
try:
    c.connect((hostname,port))
except:
    print("Connection fail.")
    exit()
c.settimeout(None)
def receive():
    i=0
    while i<3:
        i=i+1
        print(c.recv(2048).decode("utf-8"))
t(receive,())
try:
    while 1:
        c.send(input(">").encode("utf-8"))
except:
    c.close()
    exit()
