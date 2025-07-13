

import sounddevice as sd
from scipy.io.wavfile import write
import os
from datetime import datetime

# devices = sd.query_devices()
# for idx, device in enumerate(devices):
#     print(f"{idx}: {device['name']}")

# device_id = int(input("Enter input device index: "))
sd.default.device = 2 #device_id


# Set sample rate and duration
fs = 44100  # 44.1kHz
seconds = 7  # Recording time

# Create output folder
output_folder = "recordings"
os.makedirs(output_folder, exist_ok=True)

# Generate timestamped filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"recording_{timestamp}.wav"
filepath = os.path.join(output_folder, filename)

# Record
print("🎙️ Speak now...")
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()

# Save file
write(filepath, fs, recording)
print(f"✅ Recording saved as: {filepath}")

