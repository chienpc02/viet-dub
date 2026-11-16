from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
WORK_DIR = BASE_DIR / "work"
WORK_DIR.mkdir(exist_ok=True)

MODEL_SIZE = "small"              # tiny / base / small / medium / large-v3
DEFAULT_VOICE = "vi-VN-HoaiMyNeural"  # hoặc vi-VN-NamMinhNeural
MAX_SPEEDUP = 1.8                 # tốc độ đọc nhanh tối đa khi câu quá dài
