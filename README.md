# WindowsPiperTTS

A Windows application wrapper for PiperTTS with auto-download and installation of models.

Add custom models to `/models` folder within root.

```
WindowsPiperTTS/
├─ main.py            # main scrip
├─ icon.ico
├─ models/            # create this folder if need to add custom models (or app auto-creates it)
│  ├─ en_US-lessac-medium.onnx
│  ├─ en_US-lessac-medium.onnx.json
│  ├─ en_GB-cori-high.onnx
│  └─ en_GB-cori-high.onnx.json
└─ README.md
```