# SnapShield

**Private multimodal security intelligence for the AI PC era.**

> See it. Analyze it. Protect it — privately.

SnapShield is a local-first security assistant for suspicious messages and security content. It combines a compact open-source phishing classifier with a deterministic security-evidence layer covering urgency, credential/payment requests, action pressure and URL structure.

## What is real in this build

- Local transformer inference using `specific-AI/email-agent-phishing-detection`.
- Evidence-weighted risk fusion; no cloud AI API is required.
- URL structural inspection for common suspicious patterns.
- Screenshot intake UI with an explicit modular OCR/vision expansion path.
- Runtime inspection for ONNX Runtime providers, including QNN when available.
- Honest degradation: if the transformer cannot load, SnapShield does not invent an AI score.
- A benchmark helper records latency from the actual machine instead of publishing borrowed numbers.

## Run on Windows

```bat
RUN.bat
```

Or manually:

```bat
py -3.14 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app\main.py
```

The first run downloads the model checkpoint from Hugging Face and can take time depending on the connection.

## Measure the real local runtime

```bat
.venv\Scripts\activate
python benchmarks\benchmark_local.py
```

Record the output only for the machine/runtime on which it was measured. Do not reuse another device's latency as a SnapShield benchmark.

## Snapdragon deployment path

The architecture is designed for Snapdragon-powered HP PCs: model → ONNX/QNN → Qualcomm runtime → supported Snapdragon NPU → measured latency, memory and utilization. The app reports QNN availability and does **not** claim NPU execution unless the runtime actually exposes `QNNExecutionProvider`.

This distinction matters: the current development machine is not assumed to be a Snapdragon PC.

## Architecture

`Input → Local Model → Security Evidence → Risk Fusion → Human Action`

See `docs/ARCHITECTURE.md` and `docs/DEPLOYMENT.md`.

## Challenge alignment

The Snapdragon AI Lab Build & Present Challenge requires a solution designed, developed or intended to be optimized for Snapdragon-powered HP PCs. Evaluation covers technical implementation, application use case & innovation, deployment & accessibility, and presentation & documentation.

SnapShield's submission materials are included under `docs/`.

## Privacy

Sensitive content is processed locally on the selected local inference path. SnapShield is designed around minimizing unnecessary data movement. Do not paste confidential production data into a public demo or repository.

## License

MIT. See `LICENSE` if present in the repository.
