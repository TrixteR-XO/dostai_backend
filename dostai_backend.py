from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS Middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Together AI API endpoint
AI_API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = "1bbc7f2b996179192d0a5a7f16a90bd94c0dc8cd0b222080a621049f6dbdd690"  

class ChatRequest(BaseModel):
    messages: list  # Accepts full conversation history

@app.post("/api/chat")
async def chat(request: ChatRequest):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": request.messages  # Send full chat history to AI
    }

    try:
        response = requests.post(AI_API_URL, json=data, headers=headers)
        response_json = response.json()
        
        # Debugging: Print the entire response to check if API is working
        print("DEBUG: Together AI Response:", response_json)

        # Ensure valid response structure
        if "choices" in response_json and response_json["choices"]:
            reply = response_json["choices"][0]["message"]["content"]
        else:
            reply = "AI API returned an unexpected response."

        return {"reply": reply}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
