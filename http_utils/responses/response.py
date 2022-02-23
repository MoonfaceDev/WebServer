from dataclasses import dataclass, field

from http_utils.headers import Headers
from http_utils.responses.response_status import ResponseStatus


@dataclass
class Response:
    version: str = 'HTTP/1.1'
    status: ResponseStatus = ResponseStatus.OK
    headers: Headers = field(default_factory=Headers)
    body: bytes = b''

    def __post_init__(self):
        self.headers['Content-Length'] = str(len(self.body))
