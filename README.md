# Video → Phụ đề → Lồng tiếng Việt

## Cấu trúc
```
viet-dub/
├── app.py              # FastAPI: chỉ chứa các route
├── config.py           # Cấu hình (model, giọng đọc, thư mục)
├── requirements.txt
├── services/
│   ├── media.py        # ffmpeg: tách audio, tăng tốc, ghép video
│   ├── stt.py          # Giọng nói -> phụ đề (faster-whisper)
│   ├── translate.py    # Dịch sang tiếng Việt
│   └── tts.py          # Phụ đề -> giọng nói (edge-tts)
└── static/
    └── index.html      # Giao diện web
```

## Cài đặt và chạy
1. Cài Python 3.10+ và **ffmpeg** (https://ffmpeg.org/download.html)
2. `pip install -r requirements.txt`
3. `uvicorn app:app --port 8000` rồi mở http://localhost:8000

## Ghi chú
- Đổi model Whisper, giọng đọc, tốc độ tối đa trong `config.py`.
- Có GPU NVIDIA: trong `services/stt.py` dùng `WhisperModel(MODEL_SIZE, device="cuda", compute_type="float16")`.
- `deep-translator` và `edge-tts` cần có Internet.
