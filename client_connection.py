import socket
from threading import Thread

from http_utils.requests.stream_request_reader import StreamRequestReader
from http_utils.responses.stream_response_writer import StreamResponseWriter
from request_router import RequestRouter


class ClientConnection(Thread):

    def __init__(self, client_socket: socket.socket, request_router: RequestRouter) -> None:
        super().__init__()
        self._client_socket = client_socket
        self._request_router = request_router

    def run(self) -> None:
        input_stream = self._client_socket.makefile('rb')
        request_reader = StreamRequestReader(input_stream)
        request = request_reader.read()
        input_stream.close()
        print(request.method.name + ' to ' + request.route)
        callback = self._request_router.get_callback(request)
        response = callback(request)
        print(response.status.value)
        output_stream = self._client_socket.makefile('wb')
        response_writer = StreamResponseWriter(output_stream)
        response_writer.write(response)
        output_stream.close()
