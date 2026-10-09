import threading
import time
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from mcstatus import JavaServer

from src.core import game_options
from src.core import checks

is_minecraft = game_options.check_minecraft()

MINECRAFT_HOST = "athilia.duckdns.org"
MINECRAFT_PORT = 25565

app = FastAPI()

WEB_DIR = Path(__file__).resolve().parent / "front"

# =========================================================
# ПРОВЕРКА
# =========================================================
@app.get("/api/state")
def minecraft_state():
    if is_minecraft == True:
        return "ready"
    else:
        return "no_client"


# =========================================================
# МОДЕЛИ
# =========================================================

class LaunchRequest(BaseModel):
    nickname: str


# =========================================================
# FRONTEND
# =========================================================

@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")


# =========================================================
# НОВОСТИ
# =========================================================

@app.get("/api/news")
def get_news():
    return [
        {
            "id": 1,
            "tag": "update",
            "date": "29 сен",
            "title": "Новый бета лаунчер Athilia!",
            "text": "У нас появился свой лаунчер! Лучшая поддержка, бесшовные обновления и максимальное удобство!"
        },
        # {
        #     "id": 2,
        #     "tag": "event",
        #     "date": "21 сен",
        #     "title": "Зимний сезон уже близко",
        #     "text": "Готовим снег, тёплые дома и новые квесты для игроков."
        # },
        # {
        #     "id": 3,
        #     "tag": "server",
        #     "date": "14 сен",
        #     "title": "Обновление лаунчера",
        #     "text": "Новый дизайн, тёмная тема и быстрая проверка файлов."
        # }
    ]


# =========================================================
# ПРОВЕРКА ФАЙЛОВ
# =========================================================

@app.get("/api/files/check")
def check_files():
    if checks.is_minecraft_install():
        return {
            "ok": True
        }
    else:
        return {
            "ok": False
        }



# =========================================================
# ПРОВЕРКА СЕРВЕРА
# =========================================================

@app.get("/api/server/status")
def server_status():
    try:
        server = JavaServer.lookup(
            f"{MINECRAFT_HOST}:{MINECRAFT_PORT}"
        )

        status = server.status()

        return {
            "online": True,
            "players": status.players.online,
            "max": status.players.max,
            "version": status.version.name,
            "latency": round(status.latency),
        }

    except Exception as e:
        print(f"Minecraft server ping failed: {e}")

        return {
            "online": False,
            "players": 0,
            "max": 0,
            "version": None,
            "latency": None,
        }


# =========================================================
# УСТАНОВКА ИГРЫ
# =========================================================

@app.get("/api/files/install")
def game_install():
    try:
        game_options.install_minecraft()

        return {
            "ok": True
        }

    except Exception as e:
        print(f"Ошибка установки Minecraft: {e}")

        raise HTTPException(
            status_code=500,
            detail="Не удалось установить Minecraft"
        )


# =========================================================
# ЗАПУСК ИГРЫ
# =========================================================

@app.post("/api/launch")
def launch(data: LaunchRequest):
    nickname = data.nickname.strip()

    if not nickname:
        raise HTTPException(
            status_code=400,
            detail="Ник не указан"
        )

    if len(nickname) < 3 or len(nickname) > 16:
        raise HTTPException(
            status_code=400,
            detail="Ник должен содержать от 3 до 16 символов"
        )

    print(f"Запускаем Minecraft для: {nickname}")

    try:
        game_options.launch_minecraft(nickname)

    except Exception as e:
        print(f"Ошибка запуска Minecraft: {e}")

        raise HTTPException(
            status_code=500,
            detail="Не удалось запустить Minecraft"
        )

    return {
        "ok": True,
        "message": f"Minecraft запускается для {nickname}!"
    }


# =========================================================
# ОТКРЫТИЕ НОВОСТИ
# =========================================================

@app.get("/api/news/{news_id}")
def open_news(news_id: int):
    print(f"Открываем новость: {news_id}")

    return {
        "ok": True,
        "id": news_id
    }


# =========================================================
# WEB SERVER
# =========================================================

def start_backend():
    def run_server():
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8080,
            log_level="warning"
        )

    threading.Thread(
        target=run_server,
        daemon=True
    ).start()

    time.sleep(1)
