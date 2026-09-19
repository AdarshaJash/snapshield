from pathlib import Path

APP = Path(__file__).parents[1] / "app" / "main.py"
SOURCE = APP.read_text(encoding="utf-8")


def test_snapshield_security_engine():
    assert 'MODEL_ID = "specific-AI/email-agent-phishing-detection"' in SOURCE
    assert "def inspect_url(url):" in SOURCE
    assert "def security_layer(text):" in SOURCE
    assert "def analyze(text):" in SOURCE
    assert '"QNNExecutionProvider"' in SOURCE
