from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from config import get_settings

from challenges.Poke import Poke
from challenges.Wanderer import Wanderer
from challenges.Naraka import Naraka
from challenges.Niko import Niko
from challenges.Blinkpdf import BlinkPDF

import os

app = FastAPI()
security = HTTPBasic()
settings = get_settings()

challenges = {
    "poke": Poke(10000),
    "blinkpdf": BlinkPDF(11000),
    "naraka": Naraka(12000),
    "wanderer": Wanderer(13000),
    "niko": Niko(15000),
}

class Flag(BaseModel):
    flag: str
    challenge: str

class History(BaseModel):
    log: str


@app.get("/")
def read_root():
    return {"service": "receiver-service"}


@app.get("/restart/{challenge}")
def restart(challenge: str, credentials: HTTPBasicCredentials = Depends(security)):
    validate(credentials, challenge)
    os.system(f"docker compose -f {settings.COMPOSE_LOCATION} restart {challenge}")
    return {"message": "Challenge restarted"}


@app.get("/rollback/{challenge}")
def rollback(challenge: str, credentials: HTTPBasicCredentials = Depends(security)):
    validate(credentials, challenge)
    os.system(f"docker compose -f {settings.COMPOSE_LOCATION} up -d --force-recreate {challenge}")
    return {"message": "Challenge restarted"}


@app.get("/activate/{challenge}")
def activate(challenge: str, credentials: HTTPBasicCredentials = Depends(security)):
    validate(credentials, challenge)
    os.system(f"docker compose -f {settings.COMPOSE_LOCATION} up -d {challenge}")
    return {"message": "Challenge activated"}


@app.get("/deactivate/{challenge}")
def deactive(challenge: str, credentials: HTTPBasicCredentials = Depends(security)):
    validate(credentials, challenge)
    os.system(f"docker compose -f {settings.COMPOSE_LOCATION} down {challenge}")
    return {"message": "Challenge deactivated"}


@app.get("/credential/{challenge}")
def credential(challenge: str, credentials: HTTPBasicCredentials = Depends(security)):
    validate(credentials, challenge)
    return challenges[challenge].credentials()


@app.post("/flag")
def receive(data: Flag, credentials: HTTPBasicCredentials = Depends(security)):
    validate(credentials, data.challenge)
    challenge = challenges[data.challenge]
    if challenge.distribute(data.flag):
        return {"message": "Flag received"}

    raise HTTPException(status_code=500, detail="Error receiving flag")


@app.get("/check/{challenge}")
def check(challenge: str, credentials: HTTPBasicCredentials = Depends(security)):
    validate(credentials, challenge)
    return {"success": challenges[challenge].check()}

@app.post("/history")
def history(data: History):
    with open('history/command.txt', 'a') as f:
        f.write(data.log + '\n')
    return {"message": "Command received"}

def is_admin(credentials):
    if credentials.username != settings.ADMIN_USERNAME or credentials.password != settings.ADMIN_PASSWORD:
        return False
    return True


def validate(credentials, challenge):
    if not is_admin(credentials):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if challenge not in challenges:
        raise HTTPException(status_code=400, detail="Invalid challenge")
