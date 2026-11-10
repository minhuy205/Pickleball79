"""Công cụ chọn 4 góc sân bằng chuột.

Cách dùng:
    python -m tracking.calibrate video.mp4 --out data/calib.json [--frame 0]

Click 4 góc theo thứ tự: gần-trái, gần-phải, xa-phải, xa-trái.
Phím: Enter = lưu, r = chọn lại, q/Esc = thoát.
"""
from __future__ import annotations

import argparse

import cv2
import numpy as np

from .court import CourtCalibration
from .sources import VideoFileSource

LABELS = ["1 gan-trai", "2 gan-phai", "3 xa-phai", "4 xa-trai"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default="data/calib.json")
    ap.add_argument("--frame", type=int, default=0)
    args = ap.parse_args()

    with VideoFileSource(args.video) as src:
        image = src.read_frame(args.frame)
    if image is None:
        raise SystemExit("Không đọc được frame")

    points: list[tuple[int, int]] = []

    def on_mouse(event, x, y, *_):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
            points.append((x, y))

    cv2.namedWindow("calibrate")
    cv2.setMouseCallback("calibrate", on_mouse)

    while True:
        view = image.copy()
        for i, p in enumerate(points):
            cv2.circle(view, p, 6, (0, 255, 0), -1)
            cv2.putText(view, LABELS[i], (p[0] + 8, p[1] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        if len(points) == 4:
            cv2.polylines(view, [np.array(points, np.int32)], True, (0, 255, 255), 2)
        hint = f"Click goc {len(points) + 1}/4" if len(points) < 4 else "Enter = luu, r = chon lai"
        cv2.putText(view, hint, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow("calibrate", view)

        key = cv2.waitKey(30) & 0xFF
        if key == ord("r"):
            points.clear()
        elif key in (27, ord("q")):
            break
        elif key in (13, 10) and len(points) == 4:
            calib = CourtCalibration(np.array(points, np.float32))
            calib.save(args.out)
            print(f"Đã lưu {args.out}")
            cv2.imshow("top-down (kiem tra)", calib.top_down_view(image))
            print("Xem cửa sổ top-down: vạch sân phải thẳng. Nhấn phím bất kỳ để thoát.")
            cv2.waitKey(0)
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
