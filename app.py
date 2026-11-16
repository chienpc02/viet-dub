import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from config import DEFAULT_VOICE, STATIC_DIR, WORK_DIR
from services import media, stt, translate, tts

app = FastAPI()


@app.post("/api/transcribe")
def api_transcribe(file: UploadFile = File(...)):
    job = uuid.uuid4().hex[:10]
    src = WORK_DIR / f"{job}_src{Path(file.filename).suffix}"
    src.write_bytes(file.file.read())
    wav = WORK_DIR / f"{job}.wav"
    media.extract_audio(src, wav)
    segments, language = stt.transcribe(wav)
    return {"job": job, "language": language, "segments": segments}


@app.post("/api/translate")
def api_translate(data: dict):
    data["segments"] = translate.translate_segments(data["segments"])
    return data


@app.post("/api/tts")
def api_tts(data: dict):
    job = data["job"]
    audio = tts.build_voice_track(job, data["segments"], data.get("voice", DEFAULT_VOICE))
    src = next(WORK_DIR.glob(f"{job}_src*"))
    video = WORK_DIR / f"{job}_dubbed.mp4"
    media.mux(src, audio, video)
    return {"audio": f"/files/{audio.name}", "video": f"/files/{video.name}"}


app.mount("/files", StaticFiles(directory=WORK_DIR), name="files")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")
