from typing import Tuple, BinaryIO, Dict

from http_utils.headers import Headers
from http_utils.requests.request import Request
from http_utils.requests.request_exceptions import BadFormatException, UnsupportedMethodException
from http_utils.requests.request_method import RequestMethod
from http_utils.requests.request_reader import IRequestReader


class StreamRequestReader(IRequestReader):

    def __init__(self, input_stream: BinaryIO):
        self._input_stream = input_stream

    @staticmethod
    def _parse_params_line(params_line) -> Dict[str, str]:
        return {param_parts[0]: param_parts[2] for param_parts in
                [param.partition('=') for param in params_line.split('&')]}

    def _read_request_line(self) -> Tuple[RequestMethod, str, Dict[str, str], str]:
        try:
            request_line = self._input_stream.readline().decode()
        except UnicodeDecodeError:
            raise BadFormatException('Bad request format')
        request_parts = request_line.split(' ')
        if len(request_parts) not in [2, 3]:
            raise BadFormatException('Bad request format')
        try:
            method = RequestMethod[request_parts[0].strip().upper()]
        except KeyError:
            raise UnsupportedMethodException('Unsupported request method')
        route, _, params_line = request_parts[1].strip().partition('?')
        if len(params_line) > 0:
            params = self._parse_params_line(params_line)
        else:
            params = dict()
        if len(request_parts) == 3:
            version = request_parts[2].strip()
        else:
            version = 'HTTP/1.1'
        return method, route, params, version

    def _read_headers(self) -> Headers:
        headers = Headers()
        while True:
            try:
                line = self._input_stream.readline().decode()
            except UnicodeDecodeError:
                raise BadFormatException('Bad request format')
            if not line.strip():
                return headers
            header_name, _, header_value = line.partition(':')
            header_value = header_value.strip()
            headers[header_name] = header_value

    def read(self) -> Request:
        method, route, params, version = self._read_request_line()
        headers = self._read_headers()
        try:
            content_length = int(headers['Content-Length'])
        except KeyError:
            content_length = 0
        body = self._input_stream.read(content_length)
        return Request(method, route, params, version, headers, body)
