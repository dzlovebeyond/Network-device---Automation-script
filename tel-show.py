#!/usr/local/bin/python3
#-*- coding:utf-8 -*-

import telnetlib
import time
from sqlalchemy import *
from sys import argv

#操作设备的命令脚本变量
orders = """
screen-length disable
dis acl 2044
quit
"""

#定义登陆设备使用的用户名密码
username = 'user1'
password = 'XXX'

#用于telnet设备的函数
def tel_dev(hostname, dev_ip):
    print(hostname, '  ', dev_ip)
    global tn
    global msg_all
    global msg_error
    msg_all = ''
    msg_error = ''
    try:
        tn = telnetlib.Telnet(dev_ip, timeout=3)
        time.sleep(1)
        try:
            msg_dev_user = (tn.read_until(b"sername:" or b"ogin:", timeout=3)).decode('utf-8')
            tn.write(username.encode('utf-8') + b'\n')
            time.sleep(0.5)
            msg_dev_pwd = (tn.read_until(b"assword:", timeout=3)).decode('utf-8')
            tn.write(password.encode('utf-8') + b'\n')
            time.sleep(1)
            order(orders)
            msg_dev_act = tn.read_all().decode(encoding='utf-8')
            tn.close()
            msg_all = msg_dev_user + msg_dev_pwd + msg_dev_act
        except:
            msg_error = "orders error!!!"
            # print(msg_all)
            tn.close()
        # print(msg_all)
    except:
        msg_error = "Connection refused!!!"

#将命令转换成一行一行写入的命令格式
def order(orders):
    orders = orders.strip().split('\n')
    for x in orders:
        tn.write(x.encode('utf-8') + b'\n')



# ======== 程序开始执行 ======== #
print("程序开始时间：", end='')
print(time.strftime("%Y-%m-%d %H:%M:%S ",time.localtime(time.time())))

#定义IP地址文件名，并打开读取文件
filename = "ip.txt"
print('filename: ', filename, '\n')
f = open(filename, mode='r')
f_line = f.readlines()
#print(f_line)

#循环读取文件，并登陆设备修改ACL
for x in f_line:
    print('='*40)
    line = x.strip()          #去首尾无用字符
    lines = line.split(',')   #按,分割成列表
    tel_dev(lines[0],lines[1])
    # print(msg_all)
    print(msg_error)
    if('Basic' in msg_all):
        print('Have.')
    else:
        print('Not have!')

print('='*40)
f.close()

