#!/bin/python3
# -*- coding: UTF-8 -*-
codelist = r"abcdefghijklmnopqrstuvwxyz ABCDEFGHIJK-LMNOPQRSTUVWXYZ.()"
encodinglist = r"8a~sfDghjk_lwertyuiop=mnbzxc>vqZX0VBN3ASdFGHJKLP9WERTYUIO"


def encode(code):
    lenth = len(code)
    encoded = ""
    for i in range(0, lenth):
        try:
            buf = codelist.index(code[i])
            encoded = encoded+encodinglist[buf]
        except Exception:
            encoded = encoded+code[i]
    return encoded


def decode(encoding):
    lenth = len(encoding)
    code = ""
    for i in range(0, lenth):
        try:
            buf = encodinglist.index(encoding[i])
            code = code+codelist[buf]
        except Exception:
            code = code+encoding[i]
    return code

####main
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random as r

my_sender = decode('ofiow8jlifu=fu@yyU~rw')    # 发件人邮箱账号(已加密)
my_pass = decode('n_rhn_row_ilf8ga')             # 发件人邮箱密码(已加密)
#my_user='3343977167@qq.com'      # 收件人邮箱账号，我这边发送给自己
my_user = input("Receiver:")


def mail():
    ret = True
    try:
        msg=MIMEText(f'Your verification code is {r.randint(100000,999999)}.','plain','utf-8')
        msg['From']=formataddr(["Harvard University",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["User",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="Verification code"                # 邮件的主题，也可以说是标题
 
        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret
 
ret=mail()
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")
