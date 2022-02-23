from typing import Iterator, Dict, MutableMapping


class Headers(MutableMapping):

    def __init__(self, seq=None, **kwargs):
        self._data: Dict[str, str] = dict()
        self._data.update(seq or {}, **kwargs)

    def __setitem__(self, key: str, value: str) -> None:
        self._data[key.lower()] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key.lower()]

    def __getitem__(self, key: str) -> str:
        return self._data[key.lower()]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __str__(self) -> str:
        return '\r\n'.join([f'{key.capitalize()}: {value.capitalize()}' for key, value in self._data.items()]) + '\r\n'
