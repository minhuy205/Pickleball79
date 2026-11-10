# Pickleball79

Web app theo dõi trận Pickleball: quỹ đạo bóng, người đánh, tốc độ bóng.
Giai đoạn 1: video đã quay. Giai đoạn 2: live.

## Cài đặt (macOS / Apple Silicon)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Dùng thử bước 1-2

```bash
# 1. Chọn 4 góc sân trên frame đầu của video (click chuột, Enter để lưu)
python -m tracking.calibrate path/to/video.mp4 --out data/calib.json

# 2. Chạy pipeline trên toàn bộ video, ghi kết quả ra JSON Lines
python -m tracking.cli run path/to/video.mp4 --calib data/calib.json --out data/result.jsonl

# 3. Chạy API
uvicorn app.main:app --reload
# mở http://127.0.0.1:8000/docs
```

## Kiến trúc

```
FrameSource ──► Pipeline (các Stage, có trạng thái) ──► Sink
(file / stream)                                          (JSONL / DB / WebSocket)
```

`backend/tracking/` là lõi, KHÔNG import gì từ web. Video và live dùng chung lõi này,
chỉ khác FrameSource và Sink.

## Hệ toạ độ sân (mét)

Sân 6.096 m (rộng, trục x) x 13.411 m (dài, trục y). Gốc (0,0) là góc gần-trái.
Thứ tự 4 góc khi chọn: gần-trái, gần-phải, xa-phải, xa-trái (nhìn từ camera).
