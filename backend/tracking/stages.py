"""Các Stage của pipeline. Hiện chỉ có stage mẫu; thêm player/ball ở các bước sau."""
from __future__ import annotations

from .court import CourtCalibration
from .types import Frame, FrameResult


class CourtInfoStage:
    """Stage mẫu: ghi trạng thái hiệu chỉnh sân. Dùng để kiểm tra pipeline chạy thông."""

    name = "court"

    def __init__(self, calib: CourtCalibration | None):
        self.calib = calib

    def process(self, frame: Frame, result: FrameResult) -> None:
        result.data["calibrated"] = self.calib is not None
