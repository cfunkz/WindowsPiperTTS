# WindowsPiperTTS

<p align="center">
  <img width="256" height="256" alt="WindowsPiperTTS Logo" src="https://github.com/user-attachments/assets/ea5b6c51-67e9-4515-ae5f-df8d11a6a046" />
</p>

<p align="center">
  <a href="https://github.com/cfunkz/WindowsPiperTTS/releases">
    <img alt="Downloads" src="https://img.shields.io/github/downloads/cfunkz/WindowsPiperTTS/total?style=for-the-badge" />
  </a>
  <a href="https://github.com/cfunkz/WindowsPiperTTS/stargazers">
    <img alt="Stars" src="https://img.shields.io/github/stars/cfunkz/WindowsPiperTTS?style=for-the-badge" />
  </a>
  <a href="https://github.com/cfunkz/WindowsPiperTTS/network/members">
    <img alt="Forks" src="https://img.shields.io/github/forks/cfunkz/WindowsPiperTTS?style=for-the-badge" />
  </a>
  <a href="https://github.com/cfunkz/WindowsPiperTTS/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/cfunkz/WindowsPiperTTS?style=for-the-badge" />
  </a>
</p>

<p align="center">
  A Windows application wrapper for PiperTTS with auto-download and installation of models from Hugging Face. Manual model addition, text-to-speech playback, config adjustment, and WAV export.
</p>

> Add custom models to `models/` (in the app folder). folder within root.

## Get voice models manually

- [Piper (official) voice list](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/VOICES.md)
- [Hugging Face: rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices/tree/main)

## App Usage
- Download:
  - [Single Executable](https://github.com/cfunkz/WindowsPiperTTS/releases/tag/windows-single) (Not Recommended, Slow Startup)
  - [Extracted Executable](https://github.com/cfunkz/WindowsPiperTTS/releases/tag/windows) (Recommended, Instant Startup)
- Run the `PiperTTS.exe`.
- Select/download/add model.
- Enter text in box.
- Adjust config (volume, speed, noise, noise_w).
- Click "▶" for audio or "💾" to export as WAV.

## Development Setup
- Install Python 3.10+.
- Install dependencies: `pip install customtkinter piper-tts sounddevice numpy`
- Clone repo and run main.py.

## Functions
- `load_model()`: Loads selected ONNX model.
- `download_voice()`: Downloads model from Hugging Face.
- `add_model()`: Adds local models to /models.
- `play()`: Synthesizes and plays audio in a thread.
- `export_wav()`: Saves synthesized audio to WAV.
- `refresh_models()`: Updates model list.

```
WindowsPiperTTS/
├─ main.py
├─ icon.ico
├─ models/                             # create this
│  ├─ en_US-lessac-medium.onnx
│  ├─ en_US-lessac-medium.onnx.json
│  ├─ en_GB-cori-high.onnx
│  └─ en_GB-cori-high.onnx.json
└─ README.md
```

### Get voice-models automatically from hugginface.co
<img width="1149" height="752" alt="image" src="https://github.com/user-attachments/assets/3effab22-918d-49f7-9a0b-ed3efb25b879" />

### Manually upload voice models
<img width="1128" height="749" alt="image" src="https://github.com/user-attachments/assets/136f5388-ea27-46b1-bc69-8d464c018b77" />

### Play or output to file
<img width="1141" height="750" alt="image" src="https://github.com/user-attachments/assets/2f35c21d-41ba-4789-941e-bfa9cc3c72a3" />
<img width="1139" height="748" alt="image" src="https://github.com/user-attachments/assets/07510764-ef3c-4dda-810f-9ace3bba8ced" />

