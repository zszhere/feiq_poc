# !/usr/bin/env python
# coding=utf8
# @Author  : zz
# @Desc    :

import ipaddress
import binascii
import socket
import time
import sys
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED

def payload(ctl,msg):
    # sVer = '5.1.161212'
    # 我这个版本必须用这个特殊的版本号 '1_lbt8'
    sVer = '1_lbt8'
    # 时间戳
    sTime = str(int(time.time()))
    sName = 'test'
    sHost = 'test'
    # 功能码 32 为发送消息 回包 119
    # 功能码 209 为抖动屏幕 回包 210
    # 功能码 472 为心跳探测 回包 120
    # sCtl = '472'
    sCtl = ctl
    # sMsg = ''
    sMsg = msg
    send = ':'.join([sVer,sTime,sName,sHost,sCtl,sMsg])
    payload = send.encode('utf8')
    # print(payload)
    # return binascii.a2b_hex('315f6c6274365f302331323823303030433239344242434146233023302330233430303123393a313635323434373032313a7a7a3a57494e31302d57524b3a3230393a00')
    return payload

def scan(ip):
    HOST = ip
    PORT = 2425
    BUFSIZE = 1024
    TIMEOUT = 3
    ADDR = (HOST,PORT)
    Conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Conn.settimeout(TIMEOUT)
    Conn.connect(ADDR)
    # Conn.send(payload('32','hello'))
    # Conn.send(payload('209',''))
    Conn.send(payload('472',''))
    try:
        recv = Conn.recv(BUFSIZE)
        recv = recv.decode('utf8')
        recvUser = recv.split(':')[2]
        recvHost = recv.split(':')[3]
        print('[+]IP:{} USER:{} HOST:{} is online'.format(HOST,recvUser,recvHost))
        Conn.close()
    except Exception as e:
        # print(e)
        # print('[-]IP:{} is offline'.format(HOST))
        Conn.close()

# scan('172.16.170.3')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("use:python3 {} {}".format(sys.argv[0],"192.168.1.1/24"))
        sys.exit()
    ip = sys.argv[1]
    ips = ipaddress.ip_network(ip.strip(), strict=False).hosts()
    executor = ThreadPoolExecutor(max_workers=100)
    all_task = []
    sTime = time.time()
    print('[+]Scan start...')
    # for i in range(170,171):
    #     for j in range(1,10):
    #         ip = '172.16.{}.{}'.format(i,j)
    #         all_task.append(executor.submit(scan,ip))
    for i in ips:
        all_task.append(executor.submit(scan,str(i)))
    wait(all_task, return_when=ALL_COMPLETED)
    eTime = time.time()
    print('[+]Scan time: {:.2f}s.Finished.'.format(eTime-sTime))