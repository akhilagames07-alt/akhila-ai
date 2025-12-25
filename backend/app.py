import os
import openai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --------------------
# OpenAI setup
# --------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

# --------------------
# App setup
# --------------------
app = FastAPI(title="Akhila AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Request model
# --------------------
class GenerateRequest(BaseModel):
    template: str
    prompt: str

# --------------------
# Templates
# --------------------
TEMPLATES = [
    "youtube_thumbnail",
    "email",
    "ad",
    "explain_simple"
]

# --------------------
# Root
# --------------------
@app.get("/")
def root():
    return {"status": "Akhila AI running with OpenAI (classic import)"}

# --------------------
# Templates list
# --------------------
@app.get("/templates")
def get_templates():
    return {"templates": TEMPLATES}

# --------------------
# Prompt builder
# --------------------
def build_prompt(template: str, user_input: str) -> str:
    if template == "youtube_thumbnail":
        return f"""
Generate 5 viral YouTube thumbnail titles.
Topic: {user_input}
Use emojis and strong curiosity hooks.
"""

    if template == "email":
        return f"""
Write a polite and professional email.
Context: {user_input}
Tone: respectful
Include subject line.
"""

    if template == "ad":
        return f"""
Write a short marketing advertisement.
Product or idea: {user_input}
Make it catchy and persuasive.
"""

    if template == "explain_simple":
        return f"""
Explain this in very simple terms so a beginner can understand:
{user_input}
"""

    return user_input

# --------------------
# OpenAI call
# --------------------
def ask_openai(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Akhila AI, a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# --------------------
# Generate endpoint
# --------------------
@app.post("/generate")
def generate(req: GenerateRequest):
    if req.template not in TEMPLATES:
        return {"output": "Invalid template selected"}

    final_prompt = build_prompt(req.template, req.prompt)
    output = ask_openai(final_prompt)

    return {"output": output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
