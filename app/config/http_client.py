import aiohttp
import asyncio
from loguru import logger
from typing import Any

class AiohttpFactory:
    
    _instance = None
    session: aiohttp.ClientSession | None = None
    total: int = 60
    connect: int = 10
    sock_connect: int = 7
    sock_read: int = 45
    limit_per_host: int = 100
    limit: int = 500
    max_retries: int = 2
    backoff_factor: int = 2
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def start(self) -> None:
        """Открываем async session на старте приложения (инициализация на фабрике приложения)"""
        if not self.session or self.session.closed:
            timeout = aiohttp.ClientTimeout(
                                            total=self.total, 
                                            connect=self.connect, 
                                            sock_connect=self.sock_connect, 
                                            sock_read=self.sock_read
                                            )
            connector = aiohttp.TCPConnector(
                                            limit_per_host=self.limit_per_host, 
                                            limit=self.limit
                                            )
            self.session = aiohttp.ClientSession(
                                                timeout=timeout, 
                                                connector=connector
                                                )
            logger.info("Async session started.")

    async def stop(self) -> None:
        """Закрывает сессию aiohttp"""
        if self.session:
            await self.session.close()
            self.session = None

    async def fetch_data(self, method: str, url: str, content_key: str, **kwargs):
        """Базовый метод запроса с поддержкой повторных попыток"""
        attempt = 0

        while attempt <= self.max_retries:
            try:
                if not self.session or self.session.closed:
                    raise RuntimeError("Aiohttp session is not initialized. Call .start() first.")
                
                async with self.session.request(method, url, **kwargs) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return {content_key: data, "error": None, "url": url, "status": response.status}
            
            except aiohttp.ClientResponseError as e:
                logger.error(f"HTTP error {e.status}: {e.message} - {url}")
                attempt += 1
                if attempt > self.max_retries:
                    return {content_key: {}, "error": str(e), "url": url, "status": e.status}

            except aiohttp.ClientError as e:
                logger.error(f"Client error: {str(e)} - {url}")
                attempt += 1
                if attempt > self.max_retries:
                    return {content_key: {}, "error": str(e), "url": url, "status": 502}
                
            except asyncio.TimeoutError as e:
                logger.error(f"Timeout error: {str(e)} - {url}")
                attempt += 1
                if attempt >= self.max_retries:
                    return {content_key: {}, "error": "Timeout", "url": url, "status": 504}
                
            except Exception as e:
                logger.error(f"Exception: {str(e)} - {url}")
                attempt += 1
                if attempt >= self.max_retries:
                    return {content_key: {}, "error": str(e), "url": url, "status": 502}

            await asyncio.sleep(self.backoff_factor * attempt)

    async def get(self, url, content_key="content", **kwargs)->dict[str, Any]:
        headers: dict[str, str] = kwargs.pop("headers", {})
        headers.setdefault("Content-Type", "application/json")
        return await self.fetch_data("GET", url, content_key, headers=headers, **kwargs)

    async def post(self, url, body=None, content_key="content", **kwargs)->dict[str, Any]:
        headers: dict[str, str] = kwargs.pop("headers", {})
        headers.setdefault("Content-Type", "application/json")
        return await self.fetch_data("POST", url, content_key, json=body, headers=headers, **kwargs)

    async def put(self, url, body=None, content_key="content", **kwargs)->dict[str, Any]:
        headers: dict[str, str] = kwargs.pop("headers", {})
        headers.setdefault("Content-Type", "application/json")
        return await self.fetch_data("PUT", url, content_key, json=body, headers=headers, **kwargs)

    async def delete(self, url, content_key="content", **kwargs)->dict[str, Any]:
        return await self.fetch_data("DELETE", url, content_key, **kwargs)

    async def patch(self, url, body=None, content_key="content", **kwargs)->dict[str, Any]:
        headers: dict[str, str] = kwargs.pop("headers", {})
        headers.setdefault("Content-Type", "application/json")
        return await self.fetch_data("PATCH", url, content_key, json=body, headers=headers, **kwargs)

    async def head(self, url, **kwargs)->dict[str, Any]:
        return await self.fetch_data("HEAD", url, content_key="headers", **kwargs)

http_client = AiohttpFactory()