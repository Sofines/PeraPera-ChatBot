from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)  # Configure logging
logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Google AI Studio API key from .env
google_ai_studio_api_key = os.environ.get("GOOGLE_AI_STUDIO_API_KEY")
if not google_ai_studio_api_key:
    logger.error("Google AI Studio API key not found in environment variables.")
    raise ValueError("Google AI Studio API key is required.")

# Configure Google AI Studio API
genai.configure(api_key=google_ai_studio_api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-pro")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """<!DOCTYPE html>
    <html>
    <head>
        <title>Cute Japanese Tutor</title>
        <link rel="stylesheet" href="/static/style.css?v=1">
    </head>
    <body>
        <div class="chat-container">
            <h1>こんにちは！にほんごをべんきょうしましょう！</h1>
            <div class="chat-box">
                <div id="chat-log">
                    <div class="message bot-message">こんにちは！(Hello!)</div>
                </div>
                <div class="input-area">
                    <form onsubmit="sendMessage(); return false;">
                    <input type="text" id="user-input" placeholder="Type your message here...">
                    <button type="submit">Send</button>
                    </form>
                </div>
            </div>
        </div>
        <script src="/static/script.js"></script>
    </body>
    </html>"""

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "").lower()
    logger.info(f"Received user message: {user_message}")  # Log the user message

    try:
        # Generate a response using Google AI Studio
        response = model.generate_content(
            f"You are a cute Japanese tutor. Teach Japanese in a fun and simple way. User says: {user_message}"
        )
        logger.info(f"Google AI Studio API response: {response}")  # Log the entire response
        bot_response = response.text
        logger.info(f"Bot response: {bot_response}")  # Log the extracted bot message
        return JSONResponse(content={"response": bot_response})

    except Exception as e:
        logger.exception(f"Error communicating with Google AI Studio: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to generate a response"})