# # Order program

import sys
import subprocess

msg = sys.argv[1]

if msg == "start":
    # recv.pyを起動
    print("started")
    subprocess.run(['test/bin/python3', 'working/recv.py'])

else:
    from socket import socket, AF_INET, SOCK_DGRAM
    HOST = ''
    PORT = 5000
    ADDRESS = "127.0.0.1"
    s = socket(AF_INET, SOCK_DGRAM)

    s.sendto(msg.encode(), (ADDRESS, PORT))

    msg, address = s.recvfrom(8192)
    msg = msg.decode()
    print(msg)

    s.close()
