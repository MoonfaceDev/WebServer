from abc import abstractmethod

from http_utils.requests.request import Request


class IRequestReader:
    
    @abstractmethod
    def read(self) -> Request:
        pass
