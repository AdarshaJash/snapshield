# SnapShield Architecture

## Product loop

Input → Perception → Evidence → Risk Fusion → Recommendation

### Current
Text/email/SMS → phishing transformer → security evidence → risk score → action.

### Multimodal expansion
Screenshot/PDF/QR → OCR/vision → same evidence layer.

## Snapdragon

CPU: orchestration, parsing, UI  
GPU: optional visual preprocessing  
NPU: supported model inference through ONNX/QNN / Qualcomm AI runtime

## Winning benchmark plan

Measure on eligible Snapdragon hardware:
- model load time
- steady-state inference latency
- peak memory
- execution provider
- CPU utilization
- NPU utilization
- battery/power behavior where measurable

Never substitute another application's numbers for SnapShield's.
