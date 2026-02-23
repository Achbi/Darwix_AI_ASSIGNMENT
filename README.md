# 🎙️ The Empathy Engine
### Giving AI a Human Voice — Emotionally Adaptive Text-to-Speech

---

## 📌 Overview

**The Empathy Engine** is a Python-based service that dynamically modulates Text-to-Speech (TTS) vocal characteristics based on the emotional tone of input text. It bridges the gap between flat, robotic TTS output and expressive, human-like communication by detecting emotion and adapting the voice accordingly.

---

## ✨ Features

- **Multi-layer Emotion Detection** — Analyzes text at two levels:
  - *Base:* Positive, Negative, Neutral
  - *Granular:* Surprised, Inquisitive, Concerned

- **Dynamic Voice Modulation** — Adjusts speech Rate and Volume to create distinct emotional personas:

  | Emotion | Rate | Volume | Characteristic |
  |---------|------|--------|----------------|
  | Positive | Fast | High | Energetic, bright |
  | Negative | Very Slow | Soft | Heavy, subdued |
  | Surprised | Rapid | Loud | Startled, reactive |
  | Concerned | Slow | Soft | Careful, worried |
  | Inquisitive | Slightly Fast | Moderate | Engaged, curious |

- **Smart Voice Selection** — Automatically selects a female voice (e.g., "Zira" on Windows) for a warmer, more empathetic tone.

- **Web Interface** — A clean UI built with FastAPI to test the engine with real-time emotional feedback.

- **CLI Tool** — A command-line interface for quick testing and scripted usage.

---

## 🖥️ Prerequisites

- Python 3.8+
- Windows *(Recommended — best support for pyttsx3 and "Zira" voice)*, macOS, or Linux

---

## ⚙️ Setup

### 1. Navigate to the Project Directory

```bash
cd EmpathyEngine_DarwixAi
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the following packages:

| Package | Purpose |
|---------|---------|
| `pyttsx3` | Offline Text-to-Speech engine |
| `vaderSentiment` | Sentiment analysis for emotion detection |
| `fastapi` | Web framework for the UI |
| `uvicorn` | ASGI server to run FastAPI |

---

## 🚀 Usage

### Option 1 — CLI (Quick Test)

Run with text passed directly as an argument:

```bash
python command.py "I am absolutely thrilled with this result!"
```

Or run interactively and enter text when prompted:

```bash
python command.py
```

Save to a custom output path with the `-o` flag:

```bash
python command.py "This is the best news ever!" -o output/happy.wav
```

**Default output location:** `output/empathy_output.wav`

The CLI prints:
- Detected emotion
- Intensity and raw VADER compound score
- Applied rate and volume values

---

### Option 2 — Web Interface (Recommended)

Start the FastAPI server:

```bash
uvicorn web_app:app --reload
```

Then open your browser at:

```
http://127.0.0.1:8000/
```

From the web interface you can:
1. Type any message into the text area
2. Click **"Generate Emotional Voice"**
3. View the detected emotion, intensity, rate, and volume
4. Listen to the result via the embedded audio player

> Audio is stored at `output/empathy_output.wav` and served from the `/audio` endpoint.

---

## 🧠 Design Choices

**Emotion Analysis**
Combined `vaderSentiment` (for base polarity) with custom heuristics — punctuation patterns and keyword matching — to detect nuanced emotional states like Surprise and Concern that a raw sentiment score alone would miss.

**TTS Engine**
`pyttsx3` was chosen for its offline capability and cross-platform reliability. Rather than using unstable SSML tags, the engine directly modulates Rate and Volume parameters, ensuring consistent playback across all systems.

**Modulation Logic**
- **Rate** — Effectively conveys energy (fast) or sadness/concern (slow)
- **Volume** — Adds emphasis (loud) or intimacy/worry (soft)

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| No audio plays | Check that your system volume is turned up |
| `ModuleNotFoundError` | Ensure the virtual environment is active and you are inside the `empathy_engine` directory |

---

## 🧪 Example Phrases

Try these to experience the full emotional range of the engine:

```
"I'm honestly feeling very anxious about how this is going to turn out."
```
```
"Seriously? I didn't expect that at all!"
```
```
"Oh my god! That is absolutely amazing!"
```

---

## 📁 Project Structure

```
EmpathyEngine_DarwixAi/
│
├── empathy_engine.py       # Core emotion detection and TTS logic
├── web_app.py              # FastAPI web interface
├── command.py              # CLI tool
├── requirements.txt        # Python dependencies
└── output/
    └── empathy_output.wav  # Generated audio (created at runtime)
```

---

## 📦 Dependencies Summary

```
pyttsx3
vaderSentiment
fastapi
uvicorn
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

*Built with Python · pyttsx3 · vaderSentiment · FastAPI* 
Harshit Bahety
