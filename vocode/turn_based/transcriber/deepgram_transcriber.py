import io
from typing import Optional
from pydub import AudioSegment
from deepgram import DeepgramClient, FileSource, PrerecordedOptions
from vocode import getenv
from vocode.turn_based.transcriber.base_transcriber import BaseTranscriber


class DeepgramTranscriber(BaseTranscriber):
    def __init__(self, api_key: Optional[str] = None):
        api_key = getenv("DEEPGRAM_API_KEY", api_key)
        if not api_key:
            raise ValueError("Deepgram API key not provided")
        self.client = DeepgramClient(api_key=api_key)

    def transcribe(self, audio_segment: AudioSegment) -> str:
        # Export audio to memory as WAV
        in_memory_wav = io.BytesIO()
        audio_segment.export(in_memory_wav, format="wav")
        in_memory_wav.seek(0)

        # Prepare buffer and options
        payload: FileSource = {
            "buffer": in_memory_wav.read(),  # deepgram wants bytes, not a file-like object
        }

        options = PrerecordedOptions(
            model="nova-3",  # or "nova"
            smart_format=True,
            punctuate=True,
            language="en"
        )

        # Send to Deepgram
        response = self.client.listen.rest.v("1").transcribe_file(payload, options)

        # Return text
        return response["results"]["channels"][0]["alternatives"][0]["transcript"]
