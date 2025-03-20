from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PeraPera ChatBot",
    description="A cute Japanese language tutor chatbot",
    version="0.0.1",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Gemini model
try:
    google_ai_studio_api_key = os.environ.get("GOOGLE_AI_STUDIO_API_KEY")
    if not google_ai_studio_api_key:
        raise HTTPException(
            status_code=500,
            detail="Google AI Studio API key not found in environment variables",
        )
    genai.configure(api_key=google_ai_studio_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    logger.error(f"Failed to initialize Gemini model: {e}")
    raise


@app.get("/", response_class=HTMLResponse)
async def home():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found")


@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "").strip().lower()

        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        logger.info(f"Received user message: {user_message}")

        response = model.generate_content(
            f"""You are a cute Japanese  and a friend. Follow these rules:
            - Teach Japanese in a fun and simple way while being patient and friendly
            - Use emojis appropriately
            User message: {user_message}"""
        )

        bot_response = response.text
        logger.info(f"response: {bot_response}")

        return JSONResponse(content={"response": bot_response})

    except Exception as e:
        logger.exception(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response")


# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
