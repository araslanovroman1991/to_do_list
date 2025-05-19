import asyncio
import atexit
import os

from asgiref.sync import sync_to_async
from django.core.asgi import get_asgi_application  # type: ignore
from django.db import connection
from loguru import logger

from app.config.http_client import http_client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.config.settings")


@sync_to_async
def test_view():
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return {"ok": True}


async def startup():
    """Действия при старте"""
    logger.info("ASGI-APP STARTED...")
    if not http_client.session:
        await http_client.start()
    await test_view()
    logger.success("ALL SERVICES STARTED")


async def shutdown():
    """Действия при остановке"""
    logger.warning("ASGI-APP STOPPING...")
    await http_client.stop()
    logger.success("ALL SERVICES STOPPED")


atexit.register(lambda: asyncio.run(shutdown()))
django_asgi_app = get_asgi_application()


async def application(scope, receive, send):
    """ASGI-приложение"""
    if scope["type"] == "http" or scope["type"] == "websocket":
        await django_asgi_app(scope, receive, send)
    elif scope["type"] == "lifespan":
        message = await receive()
        if message["type"] == "lifespan.startup":
            await startup()
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            await shutdown()
            await send({"type": "lifespan.shutdown.complete"})
