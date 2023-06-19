# Calc program

from socket import socket, AF_INET, SOCK_DGRAM

from rinna import gettext, launch_model

HOST = ''
PORT = 5000
ADDRESS = "127.0.0.1"

s = socket(AF_INET, SOCK_DGRAM)
s.bind((HOST, PORT))

print("launch")

model, tokenizer = launch_model()

while True:
    msg, address = s.recvfrom(8192)
    msg = msg.decode('utf-8')
    if msg == "exit":
        s.sendto("finished".encode(), address)
        del model
        del tokenizer
        break

    result = gettext(msg, model, tokenizer)
    s.sendto(result.encode(), address)

s.close()
