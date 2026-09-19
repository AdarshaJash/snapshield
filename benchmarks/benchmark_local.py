"""Local SnapShield benchmark helper.
Run on the target PC to record real model latency; no benchmark numbers are hard-coded.
"""
import statistics
import time

MODEL_ID = "specific-AI/email-agent-phishing-detection"
SAMPLE = "Your account will be suspended today. Verify your credentials immediately at https://example.com/login"


def main():
    from transformers import pipeline
    pipe = pipeline("text-classification", model=MODEL_ID, truncation=True, max_length=512)
    # Warm-up
    pipe(SAMPLE)
    times = []
    for _ in range(10):
        t0 = time.perf_counter()
        pipe(SAMPLE)
        times.append((time.perf_counter() - t0) * 1000)
    print("SnapShield local benchmark")
    print(f"model={MODEL_ID}")
    print(f"runs={len(times)}")
    print(f"mean_ms={statistics.mean(times):.2f}")
    print(f"median_ms={statistics.median(times):.2f}")
    print(f"p95_ms={sorted(times)[int(len(times)*0.95)-1]:.2f}")
    print("Note: these are measurements from this machine/runtime only.")


if __name__ == "__main__":
    main()
