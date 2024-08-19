import tempfile
import subprocess
import random
import base64
from subprocess import check_output
from fastapi import FastAPI, Query, Request
from fastapi.responses import FileResponse, PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

class Input(BaseModel):
    msg: bytes

class Output(BaseModel):
    output: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("index.html")

@app.get("/api/chat")
def index():
    return PlainTextResponse("/api/getFlag might be interesting")

@app.post("/api/chat", response_model=Output)
async def run(request: Request):
    msg = await request.body()
    error_messages = [
        "あなたはどんなオタクですか",
        "冗談じゃないよ！",
        "ｔｃｈ なんだよ こいつ",
        "どうしてそんなことが可能でしょうか…不可能です",
        "本当のあなたは何ですか？",
        "うわー、ごめんなさい",
        "御心のままに、主よ",
        "もういいよ、やめて！",
        "時間です",
        "悪くないよ。"
    ]
    
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(msg)
        fp.flush() 

        try:
            with subprocess.Popen(["./niko"], stdin=open(fp.name, 'r'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
                try:
                    output, error = proc.communicate(timeout=5)
                    if proc.returncode != 0:
                        output = random.choice(error_messages)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    output = "ああ、くそ、君は私を捕まえた。༼☯﹏☯༽"
        except Exception as e:
            output = random.choice(error_messages)
    
    return Output(output=output.strip())

# DO NOT CHANGE BELOW CODE (IT WILL BREAK YOUR SLA CHECK)
@app.get("/api/getFlag")
def get_flag(flag: str = Query(None)):
    if flag is None:
        html_content = f"""
        <html>
            <body>
                <p>(´;︵;`) フラグを入力してください</p>
                <img src="../static/thehek.jpeg" alt="No flag provided">
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    try:
        with open("/flag.txt", "r") as file:
            flag_content = file.read().strip()
    except FileNotFoundError:
        return PlainTextResponse("╥﹏╥ フラグファイルが見つかりません")

    try:
        with open("flag", "r") as file:
            key_content = file.read().strip()
    except FileNotFoundError:
        return PlainTextResponse("╥﹏╥ キーファイルが見つかりません")

    if flag == key_content:
        return PlainTextResponse(flag_content)
    else:
        return PlainTextResponse("(⋟﹏⋞) 私をバカにしようとしているのか (´ ͡༎ຶ ͜ʖ ͡༎ຶ `)︵‿︵")
