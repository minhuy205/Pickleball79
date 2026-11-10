from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

import cv2

from .types import Frame


class FrameSource(ABC):
    """Nguồn frame. Video file và live stream cùng implement interface này."""

    @abstractmethod
    def frames(self) -> Iterator[Frame]: ...

    @abstractmethod
    def close(self) -> None: ...

    def __enter__(self) -> "FrameSource":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


class VideoFileSource(FrameSource):
    def __init__(self, path: str):
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise FileNotFoundError(f"Không mở được video: {path}")
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def frames(self) -> Iterator[Frame]:
        index = 0
        while True:
            ok, image = self.cap.read()
            if not ok:
                break
            # Timestamp theo FPS: ổn định hơn POS_MSEC với nhiều loại video.
            yield Frame(index=index, timestamp=index / self.fps, image=image)
            index += 1

    def read_frame(self, index: int = 0):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ok, image = self.cap.read()
        return image if ok else None

    def close(self) -> None:
        self.cap.release()


# TODO (giai đoạn live): class StreamSource(FrameSource) đọc RTSP/RTMP/WebRTC,
# gắn timestamp thời gian thực cho từng frame.
