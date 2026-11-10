from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXT = {".mp4", ".mov", ".m4v", ".avi"}

app = FastAPI(title="Pickleball79 API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/matches/upload")
async def upload_match(file: UploadFile = File(...)) -> dict:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, f"Định dạng không hỗ trợ: {ext}")
    match_id = uuid.uuid4().hex[:12]
    dest = UPLOAD_DIR / f"{match_id}{ext}"
    with dest.open("wb") as f:
        while chunk := await file.read(1024 * 1024):  # đọc từng 1 MB, không nạp cả file vào RAM
            f.write(chunk)
    # TODO: đưa job xử lý vào hàng đợi (Celery) và trả về trạng thái
    return {"match_id": match_id, "filename": dest.name, "status": "uploaded"}
