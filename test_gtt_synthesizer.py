# test_gttsynthesizer.py

from vocode.turn_based.synthesizer.gtts_synthesizer import GTTSSynthesizer
from pydub.playback import play
import time

def test_gttsynthesizer_basic():
    print("🔧 Creating synthesizer...")
    synthesizer = GTTSSynthesizer()

    test_text = "Hello! This is a test of the gTTS synthesizer."
    print(f"🗣 Synthesizing: {test_text}")
    audio = synthesizer.synthesize(test_text)

    print("🔊 Playing audio...")
    play(audio)

    print("✅ Synthesis complete.")
    time.sleep(audio.duration_seconds + 1)  # Give enough time for audio to play

if __name__ == "__main__":
    test_gttsynthesizer_basic()
