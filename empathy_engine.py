from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Tuple

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pyttsx3


class Emotion(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class EmotionResult:
    emotion: Emotion
    intensity: float  # 0.0–1.0 scaled magnitude
    raw_compound: float


class EmotionDetector:
    """
    Sentiment-based emotion detector using VADER.
    Maps text to POSITIVE / NEGATIVE / NEUTRAL with intensity scaling.
    """

    def __init__(self) -> None:
        self._analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> EmotionResult:
        scores = self._analyzer.polarity_scores(text)
        compound = scores["compound"]

        # More responsive thresholds
        if compound >= 0.1:
            emotion = Emotion.POSITIVE
        elif compound <= -0.1:
            emotion = Emotion.NEGATIVE
        else:
            emotion = Emotion.NEUTRAL

        # Ensure small emotions are still audible
        intensity = min(1.0, max(0.2, abs(compound)))

        return EmotionResult(
            emotion=emotion,
            intensity=intensity,
            raw_compound=compound,
        )


@dataclass
class VoiceProfile:
    rate: int
    volume: float  # 0.0–1.0


class EmpathyEngine:
    """
    Core Empathy Engine:
    - Detects emotion from text
    - Maps emotion to vocal parameters (rate, volume)
    - Synthesizes speech to an audio file
    """

    def __init__(self, voice_id: str | None = None) -> None:
        self.detector = EmotionDetector()
        self.engine = pyttsx3.init()

        # Capture neutral baseline
        self.base_rate: int = int(self.engine.getProperty("rate") or 200)
        self.base_volume: float = float(self.engine.getProperty("volume") or 1.0)

        if voice_id is not None:
            self.engine.setProperty("voice", voice_id)

    def emotion_to_voice(self, result: EmotionResult) -> VoiceProfile:
        """
        Improved mapping:
        - POSITIVE: much faster + louder
        - NEGATIVE: much slower + softer
        - NEUTRAL: baseline
        """

        intensity = result.intensity

        if result.emotion is Emotion.POSITIVE:
            # Up to +60% faster, +30% louder
            rate = int(self.base_rate * (1.0 + 0.6 * intensity))
            volume = min(1.0, self.base_volume + 0.3 * intensity)

        elif result.emotion is Emotion.NEGATIVE:
            # Up to -60% slower, -40% softer
            rate = int(self.base_rate * (1.0 - 0.6 * intensity))
            volume = max(0.2, self.base_volume - 0.4 * intensity)

        else:  # NEUTRAL
            rate = self.base_rate
            volume = self.base_volume

        return VoiceProfile(rate=rate, volume=volume)

    def synthesize_to_file(
        self, text: str, output_path: str | Path
    ) -> Tuple[EmotionResult, VoiceProfile, Path]:

        if not text or not text.strip():
            raise ValueError("Input text must not be empty.")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        emotion_result = self.detector.analyze(text)
        voice_profile = self.emotion_to_voice(emotion_result)

        # Apply settings
        self.engine.setProperty("rate", voice_profile.rate)
        self.engine.setProperty("volume", voice_profile.volume)

        # Slight hesitation effect for negative emotion
        speak_text = text
        if emotion_result.emotion is Emotion.NEGATIVE:
            speak_text = "..." + text

        self.engine.save_to_file(speak_text, str(output_path))
        self.engine.runAndWait()

        return emotion_result, voice_profile, output_path


def get_default_output_path() -> Path:
    """
    Default output path: ./output/empathy_output.wav
    """
    return Path("output") / "empathy_output.wav"