from enum import Enum


class ResponseStatus(Enum):
    OK = 200, 'Ok'
    NOT_FOUND = 404, 'Not found'
