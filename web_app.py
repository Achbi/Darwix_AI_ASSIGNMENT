from pathlib import Path

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse

from empathy_engine import EmpathyEngine, get_default_output_path


app = FastAPI(title="The Empathy Engine")
engine = EmpathyEngine()


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Empathy Engine</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: 'Inter', sans-serif;
      background: #f6f6f3;
      color: #1a1a1a;
      min-height: 100vh;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding: 3rem 1rem;
    }

    .card {
      background: #fff;
      border: 1px solid #e4e4e0;
      border-radius: 12px;
      padding: 2rem;
      width: 100%;
      max-width: 520px;
    }

    h1 {
      font-size: 1.1rem;
      font-weight: 600;
      color: #1a1a1a;
      margin-bottom: 0.25rem;
    }

    .sub {
      font-size: 0.8rem;
      color: #999;
      margin-bottom: 1.5rem;
    }

    textarea {
      width: 100%;
      border: 1px solid #e4e4e0;
      border-radius: 8px;
      padding: 0.85rem 1rem;
      font-family: 'Inter', sans-serif;
      font-size: 0.95rem;
      color: #1a1a1a;
      background: #fafaf8;
      resize: none;
      min-height: 140px;
      outline: none;
      transition: border-color 0.15s;
      line-height: 1.6;
    }

    textarea:focus { border-color: #1a1a1a; background: #fff; }
    textarea::placeholder { color: #bbb; }

    .row {
      display: flex;
      gap: 0.6rem;
      margin-top: 0.75rem;
    }

    button {
      border: none;
      border-radius: 7px;
      font-family: 'Inter', sans-serif;
      font-size: 0.85rem;
      font-weight: 500;
      cursor: pointer;
      transition: opacity 0.15s, background 0.15s;
    }

    .btn-go {
      flex: 1;
      background: #1a1a1a;
      color: #fff;
      padding: 0.7rem 1rem;
    }

    .btn-go:hover { opacity: 0.85; }
    .btn-go:disabled { opacity: 0.4; cursor: not-allowed; }

    .btn-clear {
      background: #f0f0ed;
      color: #666;
      padding: 0.7rem 1rem;
    }

    .btn-clear:hover { background: #e8e8e4; }

    /* Result */
    .result {
      margin-top: 1.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid #e4e4e0;
    }

    .emotion-line {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1rem;
    }

    .emotion-name {
      font-size: 1.3rem;
      font-weight: 600;
    }

    .badge {
      font-size: 0.72rem;
      font-weight: 500;
      background: #f0f0ed;
      color: #666;
      padding: 0.25rem 0.6rem;
      border-radius: 99px;
    }

    .bar-track {
      height: 4px;
      background: #f0f0ed;
      border-radius: 99px;
      margin-bottom: 1.2rem;
      overflow: hidden;
    }

    .bar-fill {
      height: 100%;
      background: #1a1a1a;
      width: {{ intensity_percent }}%;
      border-radius: 99px;
    }

    .stats {
      display: flex;
      gap: 1rem;
      margin-bottom: 1.2rem;
    }

    .stat {
      flex: 1;
      background: #fafaf8;
      border: 1px solid #e4e4e0;
      border-radius: 8px;
      padding: 0.6rem 0.8rem;
    }

    .stat-label {
      font-size: 0.68rem;
      color: #999;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.2rem;
    }

    .stat-value {
      font-size: 0.95rem;
      font-weight: 600;
    }

    audio {
      width: 100%;
      height: 36px;
    }
  </style>
</head>
<body>
<div class="card">
  <h1>Empathy Engine</h1>
  <p class="sub">Emotionally adaptive text-to-speech</p>

  <form method="post" id="form">
    <textarea name="text" id="txt" placeholder="Type something to speak aloud…">{{ text }}</textarea>
    <div class="row">
      <button type="submit" class="btn-go" id="btn">Generate Voice</button>
      <button type="button" class="btn-clear" id="clr">Clear</button>
    </div>
  </form>

  {% if audio_url %}
  <div class="result">
    <div class="emotion-line">
      <span class="emotion-name">{{ emotion }}</span>
      <span class="badge">{{ intensity }}% intensity</span>
    </div>
    <div class="bar-track"><div class="bar-fill"></div></div>
    <div class="stats">
      <div class="stat">
        <div class="stat-label">Rate</div>
        <div class="stat-value">{{ rate }} wpm</div>
      </div>
      <div class="stat">
        <div class="stat-label">Volume</div>
        <div class="stat-value">{{ volume }}</div>
      </div>
    </div>
    <audio controls autoplay>
      <source src="{{ audio_url }}" type="audio/wav"/>
    </audio>
  </div>
  {% endif %}
</div>

<script>
  document.getElementById('form').addEventListener('submit', () => {
    const b = document.getElementById('btn');
    b.textContent = 'Generating…';
    b.disabled = true;
  });
  document.getElementById('clr').addEventListener('click', () => {
    document.getElementById('txt').value = '';
    const b = document.getElementById('btn');
    b.textContent = 'Generate Voice';
    b.disabled = false;
    const r = document.querySelector('.result');
    if (r) r.style.display = 'none';
  });
</script>
</body>
</html>
"""


def render_html(
    text: str = "",
    audio_url: str | None = None,
    emotion: str | None = None,
    intensity: float | None = None,
    rate: int | None = None,
    volume: float | None = None,
) -> HTMLResponse:
    html = HTML_TEMPLATE
    intensity_percent = int((intensity or 0) * 100) if intensity is not None else 0

    replacements = {
        "{{ text }}": (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"),
        "{{ audio_url }}": audio_url or "",
        "{{ emotion }}": emotion or "",
        "{{ intensity }}": f"{intensity:.0f}" if intensity is not None else "",
        "{{ intensity_percent }}": str(intensity_percent),
        "{{ rate }}": str(rate) if rate is not None else "",
        "{{ volume }}": f"{volume:.2f}" if volume is not None else "",
    }
    for key, value in replacements.items():
        html = html.replace(key, value)

    if audio_url:
        html = html.replace("{% if audio_url %}", "")
        html = html.replace("{% endif %}", "")
    else:
        start = html.find("{% if audio_url %}")
        end = html.find("{% endif %}") + len("{% endif %}")
        if start != -1 and end != -1:
            html = html[:start] + html[end:]

    return HTMLResponse(content=html)


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return render_html()


@app.post("/", response_class=HTMLResponse)
async def generate(text: str = Form(...)) -> HTMLResponse:
    output_path = get_default_output_path()
    emotion_result, voice_profile, _ = engine.synthesize_to_file(text, output_path)
    return render_html(
        text=text,
        audio_url="/audio",
        emotion=emotion_result.emotion.value.title(),
        intensity=emotion_result.intensity,
        rate=voice_profile.rate,
        volume=voice_profile.volume,
    )


@app.get("/audio")
async def get_audio() -> FileResponse:
    path = get_default_output_path()
    if not Path(path).exists():
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="No audio generated yet.")
    return FileResponse(path, media_type="audio/wav")