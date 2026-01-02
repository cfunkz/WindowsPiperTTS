import io
import os
import sys
import threading
import shutil
import wave
from pathlib import Path
import customtkinter as ctk
import numpy as np
import sounddevice as sd
from piper import PiperVoice
from piper.config import SynthesisConfig
import piper.download_voices as piper_dl

sd.default.dtype = "int16"
sd.default.blocksize = 0
sd.default.latency = "low"

MODELS_DIR = Path(os.getenv("PIPER_MODELS_DIR", "models"))
MODELS_DIR.mkdir(parents=True, exist_ok=True)

voice = None
playing = False
stop_event = threading.Event()


def list_models():
    return sorted(p.name for p in MODELS_DIR.glob("*.onnx")) or ["No models"]


def set_status(text: str):
    status.configure(text=text)


def load_model(_=None):
    global voice
    name = model_var.get()
    if name == "No models":
        voice = None
        set_status("No model loaded")
        return

    model_path = MODELS_DIR / name
    cfg_path = model_path.with_suffix(model_path.suffix + ".json")
    if not cfg_path.exists():
        voice = None
        set_status(f"Missing config: {cfg_path.name}")
        return

    set_status("Loading…")

    def job():
        global voice
        try:
            voice = PiperVoice.load(str(model_path), config_path=str(cfg_path))
            app.after(0, set_status, f"Loaded: {name}")
        except Exception as e:
            voice = None
            app.after(0, set_status, f"Error: {e}")

    threading.Thread(target=job, daemon=True).start()


def refresh_models():
    cur = model_var.get()
    ms = list_models()
    model_menu.configure(values=ms)
    model_var.set(cur if cur in ms else ms[0])
    load_model()


def add_model():
    files = ctk.filedialog.askopenfilenames(
        title="Select Piper model files",
        filetypes=[("Piper models", "*.onnx *.json"), ("All", "*.*")],
    )
    if not files:
        return
    for src in files:
        shutil.copy2(src, MODELS_DIR / Path(src).name)
    set_status(f"Added {len(files)} file(s)")
    refresh_models()


def download_voice():
    dialog = ctk.CTkInputDialog(
        text="Enter voice id (e.g. en_US-lessac-medium):",
        title="Download Piper Voice",
    )
    voice_id = dialog.get_input()
    if not voice_id or not voice_id.strip():
        return

    voice_id = voice_id.strip()
    set_status(f"Downloading {voice_id}…")

    def job():
        argv0, out0, err0 = sys.argv, sys.stdout, sys.stderr
        buf = io.StringIO()
        try:
            sys.argv = ["piper.download_voices", voice_id, "--data-dir", str(MODELS_DIR)]
            sys.stdout = sys.stderr = buf
            try:
                piper_dl.main()
                ok = True
            except SystemExit as se:
                ok = (se.code or 0) == 0

            text = buf.getvalue().strip()
            if ok:
                app.after(0, set_status, f"Downloaded: {voice_id}")
                app.after(0, refresh_models)
            else:
                app.after(0, set_status, text or f"Download failed: {voice_id}")
        except Exception as e:
            app.after(0, set_status, f"Download error: {e}")
        finally:
            sys.argv, sys.stdout, sys.stderr = argv0, out0, err0

    threading.Thread(target=job, daemon=True).start()


def finish(stopped: bool):
    global playing
    playing = False
    stop_event.clear()
    play_btn.configure(text="▶ Play")
    set_status("Stopped" if stopped else "Ready")


def stop_play():
    if not playing:
        return
    stop_event.set()
    sd.stop()
    finish(True)


def export_wav():
    if voice is None:
        set_status("Load a voice model first")
        return
    text_val = box.get("1.0", "end").strip()
    if not text_val:
        set_status("Enter text to speak")
        return

    out = ctk.filedialog.asksaveasfilename(
        title="Save WAV",
        defaultextension=".wav",
        filetypes=[("WAV audio", "*.wav")],
        initialfile="speech.wav",
    )
    if not out:
        return

    set_status("Generating WAV…")

    def worker():
        try:
            cfg = SynthesisConfig(
                volume=vol.get(),
                length_scale=length.get(),
                noise_scale=noise.get(),
                noise_w_scale=noise_w.get(),
            )
            with wave.open(out, "wb") as wf:
                voice.synthesize_wav(text_val, wf, cfg)
            app.after(0, set_status, f"Saved: {Path(out).name}")
        except Exception as e:
            app.after(0, set_status, f"Error: {e}")

    threading.Thread(target=worker, daemon=True).start()


def play():
    global playing
    if playing:
        stop_play()
        return

    if voice is None:
        set_status("Load a voice model first")
        return

    text_val = box.get("1.0", "end").strip()
    if not text_val:
        set_status("Enter text to speak")
        return

    stop_event.clear()
    playing = True
    play_btn.configure(text="■ Stop")
    set_status("Synthesizing…")

    def worker():
        try:
            # Synthesize to memory buffer instead of disk
            cfg = SynthesisConfig(
                volume=vol.get(),
                length_scale=length.get(),
                noise_scale=noise.get(),
                noise_w_scale=noise_w.get(),
            )
            
            buf = io.BytesIO()
            with wave.open(buf, "wb") as wf:
                voice.synthesize_wav(text_val, wf, cfg)

            if stop_event.is_set():
                app.after(0, finish, True)
                return

            # Read from memory buffer
            buf.seek(0)
            with wave.open(buf, "rb") as rf:
                sr = rf.getframerate()
                raw = rf.readframes(rf.getnframes())
            
            audio = np.frombuffer(raw, dtype=np.int16)

            if stop_event.is_set():
                app.after(0, finish, True)
                return

            app.after(0, set_status, "Playing…")
            sd.play(audio, samplerate=sr, blocking=False)
            sd.wait()
            app.after(0, finish, stop_event.is_set())
        except Exception as e:
            sd.stop()
            app.after(0, set_status, f"Error: {e}")
            app.after(0, finish, True)

    threading.Thread(target=worker, daemon=True).start()


# UI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Piper TTS Speaker")
app.geometry("920x580")
try:
    app.iconbitmap("icon.ico")
except Exception:
    pass

app.protocol("WM_DELETE_WINDOW", lambda: (stop_play(), app.destroy()))

top = ctk.CTkFrame(app)
top.pack(fill="x", padx=12, pady=(10, 6))

ctk.CTkLabel(top, text="Voice Model", font=("", 13, "bold")).pack(side="left", padx=6)
model_var = ctk.StringVar(value=list_models()[0])
model_menu = ctk.CTkOptionMenu(top, values=list_models(), variable=model_var, command=load_model, width=320)
model_menu.pack(side="left", padx=6)

ctk.CTkButton(top, text="＋", width=28, command=add_model).pack(side="left", padx=(6, 2))
ctk.CTkButton(top, text="☁", width=28, command=download_voice).pack(side="left", padx=2)
ctk.CTkButton(top, text="⟳", width=28, command=refresh_models).pack(side="left", padx=(2, 0))

status = ctk.CTkLabel(top, text="Ready", text_color="gray")
status.pack(side="right", padx=10)

ctk.CTkLabel(app, text="Text to speak", font=("", 13, "bold")).pack(anchor="w", padx=14, pady=(6, 2))
box = ctk.CTkTextbox(app, height=260)
box.pack(fill="both", expand=True, padx=12, pady=(0, 10))
box.insert("1.0", "Type or paste text here.")

controls = ctk.CTkFrame(app)
controls.pack(fill="x", padx=12, pady=10)

ctk.CTkLabel(controls, text="Speech Settings", font=("", 12, "bold")).pack(anchor="w", padx=8, pady=(6, 8))
settings = ctk.CTkFrame(controls, fg_color="transparent")
settings.pack(fill="x", padx=8)

vol = ctk.DoubleVar(value=1.0)
length = ctk.DoubleVar(value=1.0)
noise = ctk.DoubleVar(value=0.667)
noise_w = ctk.DoubleVar(value=0.8)

for label, var, a, b in [
    ("Volume", vol, 0.0, 1.0),
    ("Speed", length, 0.5, 2.0),
    ("Noise", noise, 0.0, 1.5),
    ("Noise W", noise_w, 0.0, 1.5),
]:
    blk = ctk.CTkFrame(settings, fg_color="transparent")
    blk.pack(side="left", expand=True, fill="x", padx=8)
    hdr = ctk.CTkFrame(blk, fg_color="transparent")
    hdr.pack(fill="x")
    ctk.CTkLabel(hdr, text=label).pack(side="left")
    val = ctk.CTkLabel(hdr, text=f"{var.get():.2f}", text_color="gray")
    val.pack(side="right")
    ctk.CTkSlider(
        blk, from_=a, to=b, variable=var,
        command=lambda v, lab=val: lab.configure(text=f"{float(v):.2f}")
    ).pack(fill="x", pady=(6, 0))

btn_row = ctk.CTkFrame(controls, fg_color="transparent")
btn_row.pack(side="right", padx=10, pady=8)

ctk.CTkButton(btn_row, text="💾", width=42, height=42, command=export_wav).pack(side="left", padx=(0, 8))
play_btn = ctk.CTkButton(btn_row, text="▶ Play", command=play, width=160, height=42)
play_btn.pack(side="left")

load_model()
app.mainloop()