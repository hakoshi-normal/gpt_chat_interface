import socket
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

import paramiko
import asyncio

import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount(
    '/templates/static',
    StaticFiles(directory="templates/static"),
    name='static'
    )

KS = '*' # 伝送用区切り文字

s_IP = '*'
s_PORT = None # int
s_USER = "*"
s_PASS = "*"

async def send_msg_async(msg):
    ssh.exec_command(f'python3 working/trans.py {msg}')


def get_answer(msg):
    print(msg)
    start = time.time()
    _, stdout, stderr = ssh.exec_command(f'python3 working/trans.py {msg}')
    result = ''.join(stdout) + ''.join(stderr)

    if msg=="exit":
        return "終わり"
    return f'[{round(time.time()-start, 3)}]' + result[:-2]


def gene_prompt(dialogues):
    prompt = []
    for i, dialogue in enumerate(dialogues):
        data = {
            "speaker": ["ユーザー", "システム"][i%2],
            "text": dialogue
        }
        prompt.append(data)
    return prompt


@app.get("/")
async def index(request: Request):
    if request.method == 'GET':
        return templates.TemplateResponse("index.html", {
            # "text": "これはテストだっちゃよ？",
            "request": request
        })

    if request.method == 'POST':
        data = await request.form()
        text = data.get('text')
        answer = get_answer(text)

        return answer


app.add_api_route('/', index, methods=['GET', 'POST'])

if __name__ == '__main__':

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # ssh接続
    ssh.connect(s_IP, port=s_PORT, username=s_USER, password=s_PASS)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_msg_async('start'))

    connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connect_interface.connect(("8.8.8.8", 80))
    ip = connect_interface.getsockname()[0]
    connect_interface.close()

    try:
        uvicorn.run(app, host=ip, port=8000)
    except KeyboardInterrupt:
        pass
    get_answer("exit")
    ssh.close()
