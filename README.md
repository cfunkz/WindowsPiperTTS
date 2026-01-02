# WindowsPiperTTS

A Windows application wrapper for PiperTTS with auto-download and installation of models.

Add custom models to `/models` folder within root.

## Get voice models manually

- [Piper (official) voice list](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/VOICES.md)
- [Hugging Face: rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices/tree/main)


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
<img width="1143" height="759" alt="image" src="https://github.com/user-attachments/assets/853de9fb-2e3f-4a08-a7b7-6db302367529" />
