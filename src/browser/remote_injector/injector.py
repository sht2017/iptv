import inspect
from typing import Callable, Iterator


class Injector:
    _classes: dict[str, dict[str, Callable]]
    _objects: dict[str, Callable]

    def __init__(self) -> None:
        self._classes = {"_": {}}
        self._objects = {}

    def __getitem__(self, index: str) -> Callable:
        return self._objects[index]

    def __len__(self) -> int:
        return len(self._classes)

    def __iter__(self) -> Iterator[Callable]:
        return iter(self._classes.items())

    def __contains__(self, item: str) -> bool:
        return item in self._objects

    def __str__(self) -> str:
        return str(dict(self._classes))

    def _flatten(
        self, classes: dict, parent_key: str = ""
    ) -> dict[str, Callable]:
        items = []
        for key, value in classes.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(self._flatten(value, new_key).items())
            else:
                items.append((new_key, value))
        return dict(items)

    def register(self, obj: Callable) -> Callable:
        if inspect.isclass(obj):
            self._classes.setdefault(obj.__name__, {})
            for name, member in obj.__dict__.items():
                if isinstance(member, staticmethod):
                    self._classes[obj.__name__][name] = member
                    self._objects[f"{obj.__name__}.{name}"] = self._classes[
                        obj.__name__
                    ][name]
        elif inspect.isfunction(obj):
            self._classes["_"][obj.__name__] = obj
            self._objects[obj.__name__] = self._classes["_"][obj.__name__]
        return obj
