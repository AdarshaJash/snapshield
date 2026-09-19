# Snapdragon Deployment Checklist

1. Install Windows ARM64-compatible Python/runtime.
2. Install Qualcomm AI Hub / AI Hub Workbench tooling as appropriate.
3. Select an AI Hub-supported text classification model.
4. Export or obtain an ONNX-compatible artifact.
5. Compile for the target Snapdragon device with QNN.
6. Configure ONNX Runtime QNN Execution Provider.
7. Verify that inference is actually on NPU, not CPU fallback.
8. Capture repeatable latency/memory results.
9. Add only measured results to the submission.
