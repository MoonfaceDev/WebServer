from abc import abstractmethod

from http_utils.responses.response import Response


class IResponseWriter:

    @abstractmethod
    def write(self, response: Response) -> None:
        pass
