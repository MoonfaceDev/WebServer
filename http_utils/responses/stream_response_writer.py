from typing import BinaryIO

from http_utils.responses.response import Response
from http_utils.responses.response_writer import IResponseWriter


class StreamResponseWriter(IResponseWriter):

    def __init__(self, output_stream: BinaryIO) -> None:
        self._output_stream = output_stream

    def write(self, response: Response) -> None:
        response_line = ' '.join([response.version, str(response.status.value[0]), response.status.value[1]]) + '\r\n'
        self._output_stream.write(response_line.encode() + str(response.headers).encode() + b'\r\n' + response.body)
