
import re, time, math
from urllib.parse import urlparse
import streamlit as st

MODEL_ID = "specific-AI/email-agent-phishing-detection"

st.set_page_config(page_title="SnapShield", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

# ---------------- AI ENGINE ----------------
@st.cache_resource(show_spinner=False)
def load_model():
    try:
        from transformers import pipeline
        pipe = pipeline("text-classification", model=MODEL_ID, truncation=True, max_length=512)
        return pipe, None
    except Exception as e:
        return None, str(e)

def model_score(text):
    pipe, err = load_model()
    if err or pipe is None:
        return None, err
    out = pipe(text)[0]
    label = str(out["label"]).lower()
    p = float(out["score"])
    # This model's card defines True as phishing and False as not phishing.
    phishing = p if label in {"true","phishing","1","label_1"} else 1-p
    return phishing, None

URL_RE = re.compile(r"https?://[^\s<>\"]+", re.I)
URGENT = {"urgent","immediately","now","today","expires","suspended","blocked","verify","confirm","warning","limited"}
CREDENTIALS = {"password","otp","pin","cvv","card","credentials","login","username","passcode","bank","kyc"}
PRESSURE = {"click","claim","refund","prize","fee","payment","unlock","update","send","enter"}

def inspect_url(url):
    url=url.rstrip(".,);]}")
    try:
        p=urlparse(url); host=(p.hostname or "").lower()
    except Exception:
        return {"host":"unknown","score":0,"reasons":[],"url":url}
    score=0; reasons=[]
    if p.scheme!="https": score+=12; reasons.append("Transport is not HTTPS")
    if "@" in url: score+=20; reasons.append("Embedded @ can obscure the destination")
    if len(host)>35: score+=8; reasons.append("Unusually long hostname")
    if host.count(".")>=3: score+=8; reasons.append("Deep subdomain structure")
    if re.search(r"\d{1,3}(?:\.\d{1,3}){3}",host): score+=18; reasons.append("Destination uses an IP address")
    if any(x in host for x in ("bit.ly","tinyurl.com","t.co","goo.gl","is.gd")):
        score+=15; reasons.append("Link shortener hides the final destination")
    return {"host":host,"score":min(score,60),"reasons":reasons,"url":url}

def security_layer(text):
    low=text.lower(); score=0; reasons=[]; evidence=[]
    for words,title,unit,cap in [
        (URGENT,"Urgency / account pressure",3,12),
        (CREDENTIALS,"Credential / payment request",5,15),
        (PRESSURE,"Action pressure",2,8),
    ]:
        hits=sorted(w for w in words if re.search(r"\b"+re.escape(w)+r"\b",low))
        if hits:
            score += min(unit*len(hits),cap); reasons.append(title+" detected"); evidence += hits
    urls=[inspect_url(u) for u in URL_RE.findall(text)]
    for u in urls:
        score += u["score"]; reasons += u["reasons"]
    return min(score,40), list(dict.fromkeys(reasons)), list(dict.fromkeys(evidence)), urls

def analyze(text):
    t0=time.perf_counter()
    ai, ai_err=model_score(text)
    sec,reasons,evidence,urls=security_layer(text)
    if ai is None:
        # Honest degraded mode: no AI score is fabricated.
        final=min(99,sec)
        engine="Security evidence layer"
    else:
        final=max(0,min(99,round(ai*70+sec)))
        engine="Local transformer + security evidence"
    level="HIGH" if final>=70 else "MEDIUM" if final>=40 else "LOW"
    action={
        "HIGH":"Do not open the link or share credentials. Verify through a trusted official channel.",
        "MEDIUM":"Pause. Verify the sender and destination independently before taking action.",
        "LOW":"No strong phishing indicators were detected. Continue normal security hygiene."
    }[level]
    return dict(score=final,level=level,ai=ai,ai_err=ai_err,engine=engine,
                reasons=list(dict.fromkeys(reasons)),evidence=list(dict.fromkeys(evidence)),
                urls=urls,action=action,latency=round((time.perf_counter()-t0)*1000,1))

# ---------------- PREMIUM UI ----------------
st.markdown("""
<style>
:root{--bg:#06080c;--panel:#0d1118;--line:#202735;--muted:#8b97a9;--text:#f4f7fb;--accent:#8aa9ff}
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 80% -10%,#18243a 0,#07090d 34%,#06080c 70%)}
[data-testid="stHeader"]{background:rgba(6,8,12,.72)}
.block-container{max-width:1400px;padding:28px 36px 80px}
[data-testid="stSidebar"]{background:#080b10;border-right:1px solid #1c2330}
.brand{font-size:43px;font-weight:900;letter-spacing:-2.5px}
.kicker{font-size:11px;letter-spacing:2px;color:#8fa0b8;text-transform:uppercase}
.hero{padding:30px 34px;border:1px solid #222b39;border-radius:28px;background:linear-gradient(135deg,rgba(17,24,36,.96),rgba(8,11,16,.92));box-shadow:0 25px 90px rgba(0,0,0,.35)}
.badge{display:inline-block;border:1px solid #2a3444;border-radius:999px;padding:6px 11px;margin:16px 6px 0 0;color:#b9c6d8;font-size:10px;letter-spacing:1px}
.card{border:1px solid #202735;border-radius:22px;background:rgba(13,17,24,.88);padding:22px;height:100%}
.metric{font-size:46px;font-weight:900;letter-spacing:-2px}
.label{font-size:10px;letter-spacing:1.5px;color:#8491a4;text-transform:uppercase}
.muted{color:#8c98aa}
div.stButton>button{border-radius:13px;height:48px;font-weight:750;border:1px solid #2a3444}
div[data-testid="stTextArea"] textarea{border-radius:16px}
.smallcaps{font-size:10px;letter-spacing:1.4px;color:#7f8ca0;text-transform:uppercase}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ◈ SNAPSHIELD")
    st.caption("PRIVATE SECURITY INTELLIGENCE")
    st.divider()
    st.markdown("**Command Center**")
    st.markdown("Threat Analysis")
    st.markdown("Evidence")
    st.markdown("Runtime")
    st.divider()
    st.caption("Local-first by design")
    st.caption("Snapdragon deployment target")
    st.caption("No cloud API required")

st.markdown("""<div class="hero">
<div class="kicker">SNAPDRAGON AI LAB · 2026</div>
<div class="brand">SnapShield</div>
<div style="font-size:21px;margin-top:2px">Private multimodal security for the AI PC era.</div>
<div class="muted" style="margin-top:9px;max-width:820px">
Analyze suspicious messages and security content with local AI, structural evidence and an explainable decision layer — without sending sensitive content to a cloud AI service.
</div>
<span class="badge">LOCAL AI</span><span class="badge">EXPLAINABLE</span><span class="badge">PRIVACY-FIRST</span><span class="badge">SNAPDRAGON-OPTIMIZED</span>
</div>""", unsafe_allow_html=True)

st.write("")
tab1,tab2,tab3=st.tabs(["THREAT ANALYSIS","MULTIMODAL INBOX","RUNTIME"])

with tab1:
    left,right=st.columns([1.35,.65],gap="large")
    with left:
        st.markdown("### Analyze suspicious content")
        text=st.text_area("Threat content",height=240,placeholder="Paste an SMS, email, chat, or suspicious URL…",label_visibility="collapsed")
        b1,b2=st.columns(2)
        with b1:
            if st.button("Load showcase scenario",use_container_width=True):
                st.session_state["sample"]="Security Alert: Your account will be suspended today. Verify your credentials immediately at http://sbi-verify-account.example.com/login"
        with b2:
            run=st.button("Run local analysis  →",type="primary",use_container_width=True)
        if not text and "sample" in st.session_state: text=st.session_state["sample"]
    with right:
        st.markdown("### Intelligence pipeline")
        for n,title,desc in [
            ("01","Context model","Local transformer phishing classification"),
            ("02","Security graph","Urgency, credentials, URL structure"),
            ("03","Risk fusion","Evidence-weighted decision"),
            ("04","Action","Human-readable next step")]:
            st.markdown(f"**{n} · {title}**  \n<span class='muted'>{desc}</span>",unsafe_allow_html=True)
            st.write("")
        st.caption("Model: "+MODEL_ID)

    if run:
        if not text.strip():
            st.warning("Add content to analyze.")
        else:
            with st.spinner("Running local intelligence…"):
                r=analyze(text)
            st.divider()
            c1,c2,c3,c4=st.columns(4)
            ai_text="—" if r["ai"] is None else f'{round(r["ai"]*100)}%'
            cards=[
                ("RISK SCORE",f'{r["score"]}<span style="font-size:18px">/99</span>',r["level"]+" RISK"),
                ("LOCAL AI",ai_text,"phishing probability"),
                ("LATENCY",f'{r["latency"]}<span style="font-size:17px"> ms</span>',"end-to-end local"),
                ("DATA PATH","LOCAL","no cloud AI API"),
            ]
            for col,(lab,val,sub) in zip((c1,c2,c3,c4),cards):
                with col: st.markdown(f'<div class="card"><div class="label">{lab}</div><div class="metric">{val}</div><div class="muted">{sub}</div></div>',unsafe_allow_html=True)
            st.write("")
            a,b=st.columns(2,gap="large")
            with a:
                st.markdown("### Why SnapShield reached this decision")
                for x in (r["reasons"] or ["No strong security indicators detected."]): st.write("• "+x)
                if r["evidence"]: st.caption("Observed terms · "+" · ".join(r["evidence"]))
            with b:
                st.markdown("### Recommended action")
                st.info(r["action"])
                st.caption("Engine · "+r["engine"])
            if r["urls"]:
                st.markdown("### Destination intelligence")
                for u in r["urls"]:
                    st.markdown(f'<div class="card"><div class="smallcaps">URL</div><code>{u["url"]}</code><br><span class="muted">Host · {u["host"]} &nbsp; | &nbsp; contribution · {u["score"]}</span></div>',unsafe_allow_html=True)
                    for x in u["reasons"]: st.write("• "+x)
            if r["ai_err"]:
                st.warning("Local transformer unavailable in this environment. SnapShield did not fabricate an AI score; the evidence layer remained active.")

with tab2:
    st.markdown("### One security surface. Multiple threat formats.")
    x,y=st.columns([1.1,.9],gap="large")
    with x:
        img=st.file_uploader("Drop screenshot / image",type=["png","jpg","jpeg"],label_visibility="collapsed")
        if img: st.image(img,use_container_width=True)
        else: st.markdown('<div class="card" style="min-height:300px"><div class="kicker">MULTIMODAL INTAKE</div><h2>Drop a suspicious screenshot</h2><p class="muted">Fake login pages · payment prompts · scam chats · QR-code messages</p><br><b>Next local adapter</b><p class="muted">OCR + vision model → shared security evidence layer</p></div>',unsafe_allow_html=True)
    with y:
        st.markdown("### Product vision")
        st.markdown("**Text → URL → screenshot → document → QR**")
        st.write("Every modality feeds the same explainable security decision layer.")
        st.markdown("### Privacy contract")
        st.success("Sensitive security content stays local whenever the selected inference path is local.")
        st.caption("The current screenshot surface accepts the image; OCR/vision inference is modular and must be enabled with a validated local model before being claimed as active.")

with tab3:
    st.markdown("### Snapdragon runtime")
    st.markdown("SnapShield is designed around heterogeneous compute: CPU for orchestration, GPU where useful for visual processing, and the Snapdragon Hexagon NPU for supported AI inference.")
    try:
        import onnxruntime as ort
        p=ort.get_available_providers()
        st.code("\\n".join(p))
        if "QNNExecutionProvider" in p: st.success("QNN Execution Provider detected.")
        else: st.info("QNN Execution Provider not detected on this PC. NPU execution is not claimed.")
    except Exception:
        st.info("ONNX Runtime is not installed in this development environment.")
    st.markdown("**Deployment target:** Qualcomm AI Hub model → ONNX/QNN → Snapdragon NPU → measured latency, memory and utilization.")
    st.caption("No borrowed benchmark figures are presented as SnapShield results.")

st.divider()
st.markdown("**SNAPSHIELD**  ·  See it. Analyze it. Protect it — privately.")
st.caption("Built for the Snapdragon AI Lab Build & Present Challenge · 2026")
