from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from pyngrok import ngrok
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return "Hello from FastAPI and ngrok!"

@app.get("/plaintext")
async def exotel_webhook():
    # You can read request data if needed
    # form_data = await request.form()
    # caller_number = form_data.get("From")  # Exotel sends caller number

    # Respond with XML that Exotel expects
    response_xml = f"""
<Response>
    <Say voice="female">Hello, This is a response from your Exotel app.</Say>
</Response>
"""
    return PlainTextResponse(content=response_xml, media_type="application/xml")

if __name__ == "__main__":
    # Open a ngrok tunnel to the HTTP server
    public_url = ngrok.connect(8000)
    print(f"Public URL: {public_url}")
    
    # Start the FastAPI application
    print(f"ngrok tunnel endpoint: {public_url.public_url}")
    uvicorn.run(app, host="0.0.0.0", port=8000)