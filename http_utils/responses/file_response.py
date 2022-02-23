from pathlib import Path

from http_utils.responses.response import Response


class FileResponse(Response):

    def __init__(self, path: Path) -> None:
        self.path = path
        with path.open('rb') as file_stream:
            body = file_stream.read()
        super().__init__(body=body)
