
import sounddevice as sd
from vocode.turn_based.input_device.microphone_input import MicrophoneInput
from vocode.turn_based.transcriber.deepgram_transcriber import DeepgramTranscriber

# Step 1: List available input devices
devices = sd.query_devices()
input_devices = [d for d in devices if d["max_input_channels"] > 0]


# Step 1: Init microphone
# mic = MicrophoneInput.from_default_device()
mic = MicrophoneInput(input_devices[2]) #selected_device_info

# Step 2: Start recording
print("🎙️ Speak now...")
mic.start_listening()

import time
time.sleep(5)  # Record for 5 seconds

# Step 3: Stop and get audio segment
audio_segment = mic.end_listening()
print("✅ Recorded audio segment")

# Step 4: Transcribe with Deepgram
transcriber = DeepgramTranscriber("d936d0b7e6b8827137a9a7c10cf38163ed5ce2dc")
transcript = transcriber.transcribe(audio_segment)
print("📝 Transcript:", transcript)
