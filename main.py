from fastapi import FastAPI, Request
from time import time
from os import environ
import databases


from schemas import ZoomWebhookModel

app = FastAPI()


# берем параметры БД из переменных окружения
DB_USER = environ.get("POSTGRES_USER", "user")
DB_PASSWORD = environ.get("POSTGRES_PASSWORD", "password")
DB_HOST = environ.get("POSTGRES_HOST", "localhost")
DB_NAME = environ.get("POSTGRES_DB", "localhost")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
# создаем объект database, который будет использоваться для выполнения запросов
database = databases.Database(SQLALCHEMY_DATABASE_URL)


# ZOOM_WEBHOOK_AUTHORIZATION_TOKEN = 'ajFDq6vPRWSu5Zco9LD1ZA'  # TODO move .env


@app.on_event("startup")
async def startup():
    # когда приложение запускается устанавливаем соединение с БД
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    # когда приложение останавливается разрываем соединение с БД
    await database.disconnect()


@app.post("/api/zoom/webhook/")
async def zoom_webhook(wb_schema: ZoomWebhookModel):
    import json
    from models import zoom_events_table

    payload_post = json.loads(wb_schema.json())

    query = zoom_events_table.insert().values(
        event_ts=payload_post['event_ts'],
        event=payload_post['event'],
        payload=payload_post['payload'],
    )
    zoom_event_id = await database.execute(query)
    return {"timestamp": str(time())}
