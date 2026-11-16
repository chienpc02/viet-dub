"""Phụ đề tiếng Việt -> giọng nói, ghép theo mốc thời gian."""
import asyncio
from pathlib import Path

import edge_tts
from pydub import AudioSegment

from config import DEFAULT_VOICE, MAX_SPEEDUP, WORK_DIR
from services.media import speed_up


async def _synth(text: str, path: Path, voice: str):
    await edge_tts.Communicate(text, voice).save(str(path))


def _fit_to_slot(audio_path: Path, slot_ms: float, job: str, i: int) -> AudioSegment:
    audio = AudioSegment.from_file(audio_path)
    if slot_ms > 300 and len(audio) > slot_ms:
        rate = min(len(audio) / slot_ms, MAX_SPEEDUP)
        fast = WORK_DIR / f"{job}_{i}_f.mp3"
        speed_up(audio_path, fast, rate)
        audio = AudioSegment.from_file(fast)
    return audio


def build_voice_track(job: str, segments: list, voice: str = DEFAULT_VOICE) -> Path:
    segs = [s for s in segments if s["vi"].strip()]
    total = int(max(s["end"] for s in segs) * 1000) + 5000
    track = AudioSegment.silent(total)

    for i, s in enumerate(segs):
        p = WORK_DIR / f"{job}_{i}.mp3"
        asyncio.run(_synth(s["vi"], p, voice))
        clip = _fit_to_slot(p, (s["end"] - s["start"]) * 1000, job, i)
        track = track.overlay(clip, position=int(s["start"] * 1000))

    out = WORK_DIR / f"{job}_vi.mp3"
    track.export(out, format="mp3")
    return out
