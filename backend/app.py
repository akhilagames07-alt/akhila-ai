from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai

# 🔑 API KEY FROM ENV (already set by you)
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="Akhila AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    template: str
    prompt: str

TEMPLATE_RULES = {
    "chat": "Reply like a friendly AI assistant 😊",
    "email": "Write a professional email with subject and emojis ✉️",
    "blog": "Write a blog with headings, bullets, and emojis ✍️🔥",
    "ad": "Write a persuasive advertisement with emojis 📢🔥",
    "youtube_thumbnail": "Generate 5 YouTube thumbnail titles in ALL CAPS with emojis 🎬🔥"
}

@app.get("/")
def root():
    return {"status": "Akhila AI backend running 🚀"}

@app.post("/generate")
def generate(req: GenerateRequest):
    system_prompt = TEMPLATE_RULES.get(req.template, "Be helpful")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.prompt}
        ],
        temperature=0.8
    )

    return {
        "output": response["choices"][0]["message"]["content"]
    }
