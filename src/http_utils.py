import json

from logging import Logger

from abc import ABC, abstractmethod

from typing import Dict, Optional

from datetime import datetime

import aiohttp


class HTTPResponse:
    def __init__(self, url: str, status_code: int, body: bytes, duration: float) -> None:
        self.__url = url
        self.__status_code = status_code
        self.__body = body
        self.__duration = duration

    @property
    def url(self) -> int:
        return self.__url

    @property
    def status_code(self) -> int:
        return self.__status_code

    @property
    def body(self) -> bytes:
        return self.__body

    @property
    def duration(self) -> float:
        return self.__duration

    def to_dict(self):
        return {
            'url': self.url,
            'code': self.status_code,
            'body': '{}[...]{}'.format(self.body[:10].decode(), self.body[-10:].decode()),
            'duration': self.duration,
        }

    def __str__(self):
        return json.dumps({
            'HTTPResponse': self.to_dict()
        })


class HTTPClient(ABC):

    @abstractmethod
    async def fetch(self, url: str, method: str, body: Optional[str] = None, headers: Optional[Dict[str, str]] = None) -> HTTPResponse:
        pass


class AIOHTTPClient(HTTPClient):
    def __init__(self, timeout: float, logger: Logger):
        self.__timeout = timeout
        self.__logger = logger

    async def fetch(self, url: str, method: str, body: Optional[str]=None, headers: Optional[Dict[str, str]]=None) -> HTTPResponse:
        async with aiohttp.ClientSession(read_timeout=self.__timeout, conn_timeout=self.__timeout) as session:
            start_time = datetime.now()
            async with session.request(
                url=url,
                method=method,
                data=body,
                headers=headers
            ) as response:
                end_time = datetime.now()
                duration = (end_time - start_time).microseconds / 1e6
                body = await response.text(encoding='utf-8')
                http_response = HTTPResponse(url, response.status, body.encode('utf-8'), duration)
                self.__logger.debug(http_response)
            return http_response
