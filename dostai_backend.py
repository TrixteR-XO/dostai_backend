from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from all frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Together AI API endpoint
AI_API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = "1bbc7f2b996179192d0a5a7f16a90bd94c0dc8cd0b222080a621049f6dbdd690"

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
    "model": "mistralai/Mistral-7B-Instruct-v0.1",
    "messages": [
        {"role": "system", "content": "You are dostAI, a helpful AI assistant for india developed by Likhit. You are still in prototype mode, but you aim to provide accurate and helpful responses."},
        {"role": "user", "content": request.message}
    ]
}



    try:
        response = requests.post(AI_API_URL, json=data, headers=headers)
        response_json = response.json()
        reply = response_json.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I couldn't understand that.")
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
