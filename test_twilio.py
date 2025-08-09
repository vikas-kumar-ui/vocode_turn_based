from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from pyngrok import ngrok
from groq_llm import get_llm_response
import uvicorn

app = FastAPI()

def chunk_text(text, chunk_size=400):
    """Split text into smaller chunks for Twilio <Say>."""
    words = text.split()
    chunks, chunk = [], ""
    for word in words:
        if len(chunk) + len(word) + 1 > chunk_size:
            chunks.append(chunk)
            chunk = word
        else:
            chunk += " " + word if chunk else word
    if chunk:
        chunks.append(chunk)
    return chunks

@app.post("/voice")
async def voice(request: Request):
    """
    Handles incoming voice calls.
    Says a message and then gathers user's speech input.
    """
    response = VoiceResponse()

    # Get the form data from Twilio's request
    form_data = await request.form()

    if "SpeechResult" in form_data:
        # If Twilio returned speech input, process it
        speech_result = form_data["SpeechResult"]
        print(f"User said: {speech_result}")

        # Get Groq response
        resp = get_llm_response(speech_result)

        # Speak it in chunks to avoid Twilio truncation
        for chunk in chunk_text(resp):
            response.say(chunk, voice="alice")

        # Redirect to ask again
        response.redirect("/voice")

    else:
        # Initial call — ask user for speech
        gather = Gather(
            input="speech",
            timeout=5,
            action="/voice",
            method="POST"
        )
        gather.say("Hello! I am Pranav. Please say something after the beep.")
        response.append(gather)

        # If no input, re-prompt
        response.redirect("/voice")

    return Response(content=str(response), media_type="application/xml")


@app.get("/voice")
async def voice_get():
    response = VoiceResponse()
    response.say("Hello! I am Pranav, this call will end.", voice='alice')
    return Response(content=str(response), media_type="application/xml")


if __name__ == "__main__":
    # Open ngrok tunnel
    public_url = ngrok.connect(8000).public_url
    print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:8000\"")
    print(f" * Use this URL in Twilio webhook: {public_url}/voice")

    uvicorn.run(app, host="0.0.0.0", port=8000)
