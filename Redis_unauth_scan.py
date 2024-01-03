#!/usr/bin/env python
#coding=utf-8
#author:B1anda0
import socket
import sys
import colorama
from colorama import *
import time

init(autoreset=True)
banner='''
 _____          _ _                                    _   _     
|  __ \        | (_)                                  | | | |    
| |__) |___  __| |_ ___ ______ _   _ _ __   __ _ _   _| |_| |__  ______  ___   ___  __ _ _ __
|  _  // _ \/ _` | / __|______| | | | '_ \ / _` | | | | __| '_ \ ______ / __| / __|/ _` | '_ \
| | \ \  __/ (_| | \__ \      | |_| | | | | (_| | |_| | |_| | | |       \__ \| |__| (_| | | | |
|_|  \_\___|\__,_|_|___/       \__,_|_| |_|\__,_|\__,_|\__|_| |_|       |___/ \___|\__,_|_| |_|
'''
# 根据时间戳生成结果文件
def time_file():
    return "result_" + str(int(time.time())) + ".txt"

def check(ip, port, time_file, timeout=10):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        payload = 'info\r\n'
        s.send(payload.encode())
        result = s.recv(1024).decode()
        if 'redis_version' in result:
            print(u"\033[1;31;40m[+]{}:{}存在未授权访问漏洞".format(ip, port))
            with open(time_file, 'a') as file:
                file.write(f"{ip}:{port}\n")
        else:
            print('[-]{}:{} None'.format(ip, port))
    except (socket.error, socket.timeout):
        print(u"[-]{}:{} 请求超时".format(ip, port))

def print_help():
    print('''Example: 
                 python Redis-unauth-scan.py -u ip:port 
                 python Redis-unauth-scan.py -r url.txt
              ''')

if __name__ == '__main__':
    print(banner)
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print_help()
    elif sys.argv[1] == '-u':
        ip_port = sys.argv[2].split(':')
        if len(ip_port) == 2:
            ip = ip_port[0]
            port = ip_port[1]
            results_file = time_file()
            check(ip, port, results_file, timeout=10)
        else:
            print('格式错误！')
            print_help()
        print('Scan Over')
    elif sys.argv[1] == '-r':
        file_name = sys.argv[2]
        try:
            with open(file_name, 'r') as file:
                results_file = time_file()
                for line in file:
                    ip_port = line.strip().split(':')
                    if len(ip_port) == 2:
                        ip = ip_port[0]
                        port = ip_port[1]
                        check(ip, port, results_file, timeout=10)
                    else:
                        print('格式错误！')
                        print_help()
                print('Scan Over')
        except FileNotFoundError:
            print(f'File {file_name} not found.')
    else:
        print('参数错误！')
        print_help()
    
