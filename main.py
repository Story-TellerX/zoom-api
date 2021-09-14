from fastapi import FastAPI, Request
from time import time

from pydantic import BaseModel


class ZoomWebhookModel(BaseModel):
    event: str
    event_ts: int
    payload: dict


app = FastAPI()


@app.post("/api/zoom/webhook/")
async def zoom_webhook(payload: ZoomWebhookModel):
    print(payload.event)
    print(payload.event_ts)
    print(payload.payload)
    return {"timestamp": str(time())}
