"""Giọng nói -> phụ đề (faster-whisper)."""
from pathlib import Path

from faster_whisper import WhisperModel

from config import MODEL_SIZE

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = WhisperModel(MODEL_SIZE, compute_type="int8")
    return _model


def transcribe(wav: Path):
    segs, info = _get_model().transcribe(str(wav), vad_filter=True)
    segments = [
        {"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(), "vi": ""}
        for s in segs
    ]
    return segments, info.language
