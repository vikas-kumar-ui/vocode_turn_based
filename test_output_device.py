# test_speaker_output.py

from pydub import AudioSegment
from gtts import gTTS
from io import BytesIO
from vocode.turn_based.output_device.speaker_output import SpeakerOutput  # update if your file has a different name
import time

def test_speaker_output():
    print("🔊 Testing SpeakerOutput...")

    # 1. Create test audio with gTTS
    text = "Hello, this is a speaker output test!"
    tts = gTTS(text)
    audio_io = BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    audio_segment = AudioSegment.from_mp3(audio_io)

    # 2. Create output device from default
    output_device = SpeakerOutput.from_default_device()

    # 3. Send audio to speaker
    print("🎧 Playing audio...")
    output_device.send_audio(audio_segment)

    # Wait long enough for full playback (not strictly needed)
    time.sleep(audio_segment.duration_seconds + 1)

    # 4. Close the stream
    output_device.terminate()
    print("✅ Speaker output test completed.")

if __name__ == "__main__":
    test_speaker_output()
