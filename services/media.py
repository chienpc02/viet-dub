"""Các thao tác ffmpeg."""
import subprocess
from pathlib import Path


def run_ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", *args], check=True, capture_output=True)


def extract_audio(src: Path, wav: Path):
    run_ffmpeg("-i", str(src), "-vn", "-ac", "1", "-ar", "16000", str(wav))


def speed_up(src: Path, dst: Path, rate: float):
    run_ffmpeg("-i", str(src), "-filter:a", f"atempo={rate:.2f}", str(dst))


def mux(video: Path, audio: Path, out: Path):
    """Thay audio của video bằng audio mới."""
    run_ffmpeg("-i", str(video), "-i", str(audio), "-map", "0:v", "-map", "1:a",
               "-c:v", "copy", "-c:a", "aac", "-shortest", str(out))
