"""CLI chạy pipeline trên video: python -m tracking.cli run video.mp4 --calib data/calib.json"""
from __future__ import annotations

import argparse

from .court import CourtCalibration
from .pipeline import Pipeline
from .sinks import JsonLinesSink
from .sources import VideoFileSource
from .stages import CourtInfoStage


def main() -> None:
    ap = argparse.ArgumentParser(prog="tracking")
    sub = ap.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="Chạy pipeline trên video")
    run.add_argument("video")
    run.add_argument("--calib", help="File JSON hiệu chỉnh sân")
    run.add_argument("--out", default="data/result.jsonl")
    args = ap.parse_args()

    calib = CourtCalibration.load(args.calib) if args.calib else None
    stages = [CourtInfoStage(calib)]  # Sau này thêm: PlayerStage, BallStage, EventStage...
    pipeline = Pipeline(stages)

    with VideoFileSource(args.video) as src:
        print(f"Video: {src.width}x{src.height} @ {src.fps:.1f}fps, ~{src.total_frames} frames")
        n = pipeline.run(
            src,
            JsonLinesSink(args.out),
            on_progress=lambda c: print(f"\r{c} frames", end="") if c % 50 == 0 else None,
        )
    print(f"\nXong: {n} frames -> {args.out}")


if __name__ == "__main__":
    main()
