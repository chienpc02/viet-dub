"""Dịch phụ đề sang tiếng Việt."""
from deep_translator import GoogleTranslator


def translate_segments(segments: list) -> list:
    tr = GoogleTranslator(source="auto", target="vi")
    for s in segments:
        s["vi"] = tr.translate(s["text"]) if s["text"] else ""
    return segments
