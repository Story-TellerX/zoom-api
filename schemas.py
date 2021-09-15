from pydantic import BaseModel


class ZoomWebhookModel(BaseModel):
    event: str
    event_ts: int
    payload: dict
