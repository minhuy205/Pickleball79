from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class Frame:
    """Một frame video kèm timestamp (giây). Timestamp cần thiết để tính tốc độ."""
    index: int
    timestamp: float
    image: np.ndarray  # BGR, HxWx3


@dataclass
class FrameResult:
    """Kết quả xử lý của một frame. Các Stage ghi dữ liệu vào `data`."""
    frame_index: int
    timestamp: float
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"frame": self.frame_index, "t": round(self.timestamp, 4), **self.data}
