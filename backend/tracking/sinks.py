from __future__ import annotations

import json
from abc import ABC, abstractmethod

from .types import FrameResult


class Sink(ABC):
    """Nơi nhận kết quả. Video: ghi file/DB. Live: đẩy qua WebSocket."""

    @abstractmethod
    def write(self, result: FrameResult) -> None: ...

    def close(self) -> None:
        pass


class JsonLinesSink(Sink):
    def __init__(self, path: str):
        self._f = open(path, "w", encoding="utf-8")

    def write(self, result: FrameResult) -> None:
        self._f.write(json.dumps(result.to_dict()) + "\n")

    def close(self) -> None:
        self._f.close()


# TODO: DatabaseSink (MySQL) và WebSocketSink (live).
