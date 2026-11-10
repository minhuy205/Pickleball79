from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

# Sân Pickleball: 20 ft x 44 ft
COURT_WIDTH_M = 6.096   # trục x
COURT_LENGTH_M = 13.411  # trục y
NET_Y_M = COURT_LENGTH_M / 2

# Thứ tự góc: gần-trái, gần-phải, xa-phải, xa-trái (nhìn từ camera)
COURT_CORNERS_M = np.array(
    [[0, 0], [COURT_WIDTH_M, 0], [COURT_WIDTH_M, COURT_LENGTH_M], [0, COURT_LENGTH_M]],
    dtype=np.float32,
)


class CourtCalibration:
    """Chuyển đổi giữa pixel và toạ độ sân (mét) bằng homography.

    Lưu ý: chính xác cho điểm nằm TRÊN MẶT SÂN (chân người chơi, điểm bóng nảy).
    Bóng đang bay trên không sẽ bị lệch, cần xử lý riêng ở bước tính tốc độ.
    """

    def __init__(self, image_points: np.ndarray):
        pts = np.asarray(image_points, dtype=np.float32).reshape(4, 2)
        self.image_points = pts
        self.H, _ = cv2.findHomography(pts, COURT_CORNERS_M)
        self.H_inv = np.linalg.inv(self.H)

    def to_court(self, points_px) -> np.ndarray:
        pts = np.asarray(points_px, dtype=np.float32).reshape(-1, 1, 2)
        return cv2.perspectiveTransform(pts, self.H).reshape(-1, 2)

    def to_image(self, points_m) -> np.ndarray:
        pts = np.asarray(points_m, dtype=np.float32).reshape(-1, 1, 2)
        return cv2.perspectiveTransform(pts, self.H_inv).reshape(-1, 2)

    def top_down_view(self, image: np.ndarray, px_per_m: int = 60) -> np.ndarray:
        """Ảnh sân nhìn từ trên xuống, dùng để kiểm tra hiệu chỉnh bằng mắt."""
        scale = np.diag([px_per_m, px_per_m, 1.0])
        size = (int(COURT_WIDTH_M * px_per_m), int(COURT_LENGTH_M * px_per_m))
        return cv2.warpPerspective(image, scale @ self.H, size)

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps({"image_points": self.image_points.tolist()}, indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "CourtCalibration":
        data = json.loads(Path(path).read_text())
        return cls(np.array(data["image_points"], dtype=np.float32))
