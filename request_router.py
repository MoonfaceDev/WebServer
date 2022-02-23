from typing import Callable, Tuple, List

from http_utils.requests.request import Request
from http_utils.requests.request_method import RequestMethod
from http_utils.responses.response import Response
from http_utils.responses.response_status import ResponseStatus

RequestCallback = Callable[[Request], Response]


class RequestRouter:

    def __init__(self):
        self._request_callbacks: List[Tuple[RequestMethod, str, RequestCallback]] = list()

    def register_callback(self, method: RequestMethod, route: str, callback: RequestCallback) -> None:
        self._request_callbacks.append((method, route, callback))

    def get_callback(self, request: Request) -> RequestCallback:
        def default_callback(_: Request) -> Response:
            return Response(status=ResponseStatus.NOT_FOUND,
                            body=b'<html><head></head><body><h1>Page not found</h1></body></html>')
        for request_callback in self._request_callbacks:
            method, route, callback_function = request_callback
            if method == request.method and route == request.route:
                return callback_function
        return default_callback
