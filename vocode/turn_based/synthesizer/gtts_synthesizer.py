from io import BytesIO
from os import PathLike
from typing import Any

from pydub import AudioSegment

from vocode.turn_based.synthesizer.base_synthesizer import BaseSynthesizer


class GTTSSynthesizer(BaseSynthesizer):
    def __init__(self):
        from gtts import gTTS

        self.gTTS = gTTS

    def synthesize(self, text) -> AudioSegment:
        tts = self.gTTS(text)
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        audio = AudioSegment.from_mp3(audio_file)  # type: ignore

        # Speed up the audio by 1.2x (adjust factor as needed)
        faster_audio = self._speed_up(audio, speed=1.1)
        return faster_audio
    
    def _speed_up(self, sound: AudioSegment, speed: float) -> AudioSegment:
        # Manipulate frame rate to change speed
        new_frame_rate = int(sound.frame_rate * speed)
        return sound._spawn(sound.raw_data, overrides={"frame_rate": new_frame_rate}).set_frame_rate(sound.frame_rate)