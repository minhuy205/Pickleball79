from __future__ import annotations

from typing import Protocol

from .sinks import Sink
from .sources import FrameSource
from .types import Frame, FrameResult


class Stage(Protocol):
    """Một bước xử lý, có thể giữ trạng thái giữa các frame (tracker, Kalman...)."""

    name: str

    def process(self, frame: Frame, result: FrameResult) -> None: ...


class Pipeline:
    """Chạy lần lượt các Stage trên từng frame. Cùng một Pipeline dùng cho video và live."""

    def __init__(self, stages: list[Stage]):
        self.stages = stages

    def process_frame(self, frame: Frame) -> FrameResult:
        result = FrameResult(frame_index=frame.index, timestamp=frame.timestamp)
        for stage in self.stages:
            stage.process(frame, result)
        return result

    def run(self, source: FrameSource, sink: Sink, on_progress=None) -> int:
        count = 0
        try:
            for frame in source.frames():
                sink.write(self.process_frame(frame))
                count += 1
                if on_progress:
                    on_progress(count)
        finally:
            sink.close()
        return count
