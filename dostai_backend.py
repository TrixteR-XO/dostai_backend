from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS Middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change this for security if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Together AI API endpoint
AI_API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = "your-together-ai-key"  # Replace with your API key

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": request.message}]
    }

    try:
        response = requests.post(AI_API_URL, json=data, headers=headers)
        response_json = response.json()
        
        # Handle potential API response errors
        if "choices" in response_json and response_json["choices"]:
            reply = response_json["choices"][0].get("message", {}).get("content", "Sorry, I couldn't understand that.")
        else:
            reply = "Sorry, I couldn't understand that."

        return {"reply": reply}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
