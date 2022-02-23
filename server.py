import socket
from pathlib import Path
from typing import Callable, List, Optional

from client_connection import ClientConnection
from http_utils.requests.request import Request
from http_utils.requests.request_method import RequestMethod
from http_utils.responses.file_response import FileResponse
from http_utils.responses.response import Response
from request_router import RequestRouter, RequestCallback


class Server:

    def __init__(self) -> None:
        self._request_router = RequestRouter()
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def register_callback(self, method: RequestMethod, route: str, callback: RequestCallback) -> None:
        self._request_router.register_callback(method, route, callback)

    def get(self, route: str) -> Callable:
        def get_route(callback: Callable) -> None:
            self.register_callback(RequestMethod.GET, route, callback)

        return get_route

    def post(self, route: str) -> Callable:
        def post_route(callback: Callable) -> None:
            self.register_callback(RequestMethod.POST, route, callback)

        return post_route

    @staticmethod
    def _recursive_dirlist(directory_path: Path) -> List[Path]:
        return [file_path for file_path in directory_path.rglob('*') if file_path.is_file()]

    def serve_file(self, file_path: Path, route: str) -> None:
        def callback(_: Request) -> Response:
            return FileResponse(file_path)
        self.register_callback(RequestMethod.GET,
                               route,
                               callback)

    def serve_directory(self, directory_path: Path, root_page_path: Optional[Path] = None) -> None:
        file_paths = self._recursive_dirlist(directory_path)
        for file_path in file_paths:
            self.serve_file(file_path, '/' + str(file_path.relative_to(directory_path)).replace('\\', '/'))
        if root_page_path is not None:
            self.serve_file(root_page_path, '/')

    def run(self, host='0.0.0.0', port=80) -> None:
        self._server_socket.bind((host, port))
        self._server_socket.listen(5)
        while True:
            client_socket, client_address = self._server_socket.accept()
            client_connection = ClientConnection(client_socket, self._request_router)
            client_connection.start()
