import json
from collections.abc import MutableMapping
from io import TextIOWrapper
from typing import Any, Iterable


class JsonDB(MutableMapping):
    _file: TextIOWrapper
    _data: dict

    def __getitem__(self, key) -> Any:
        return self._data[key]

    def __setitem__(self, key, value) -> None:
        self._data[key] = value

    def __delitem__(self, key) -> None:
        del self._data[key]

    def __iter__(self) -> Iterable:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key) -> bool:
        return key in self._data

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return repr(self._data)

    def __init__(self, path: str) -> None:
        try:
            self._file = open(path, "r+", encoding="utf-8")
            self._data = json.load(self._file)
        except FileNotFoundError:
            self._file = open(path, "w+", encoding="utf-8")
            self._data = {}

    def __del__(self) -> None:
        try:
            self._file.seek(0)
            json.dump(
                self._data,
                self._file,
                ensure_ascii=False,
                indent=4,
            )
            self._file.truncate()
        finally:
            self._file.close()
