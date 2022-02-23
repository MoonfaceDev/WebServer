from dataclasses import dataclass
from typing import Dict

from http_utils.headers import Headers
from http_utils.requests.request_method import RequestMethod


@dataclass
class Request:
    method: RequestMethod
    route: str
    params: Dict[str, str]
    version: str
    headers: Headers
    body: bytes
