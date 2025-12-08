import requests
from django.conf import settings

GROQ_API_KEY = settings.GROQ_API_KEY
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
}

def call_groq(prompt):
    if not GROQ_API_KEY:
        return "GROQ API key not found."

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are an expert ATS resume writer."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
        "max_tokens": 350,
    }

    try:
        r = requests.post(GROQ_URL, headers=HEADERS, json=payload, timeout=30)
        if r.status_code != 200:
            print("GROQ ERROR:", r.text)
            return "Failed to generate AI content. Please check API key or logs."
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("GROQ EXCEPTION:", e)
        return "Failed to generate AI content. Please check API key or logs."

def generate_summary(job_title, skills, years):
    prompt = (
    f"Write a concise ATS-optimized resume summary for a "
    f"{job_title} with {years} years of experience.\n"
    f"Skills: {skills}.\n\n"
    f"RULES:\n"
    f"- 3 to 4 lines only\n"
    f"- No headings\n"
    f"- No introductory phrases\n"
    f"- No mentions of resume or summary\n"
    )
  
    return call_groq(prompt)

def optimize_experience(experience_text, job_title):
    prompt = (
    f"Rewrite the following experience into strong ATS-optimized bullet points "
    f"for a {job_title} role.\n"
    f"RULES:\n"
    f"- Return only bullet points\n"
    f"- No introduction or conclusion\n"
    f"- No explanations\n"
    f"- Start each point with an action verb\n\n"
    f"{experience_text}"
    )
    return call_groq(prompt)

def suggest_keywords(job_title, skills):
    prompt = (
    f"Generate 15 to 20 ATS-friendly keywords for a {job_title} role. "
    f"Existing skills: {skills}. "
    f"OUTPUT RULES:\n"
    f"- Output keywords only\n"
    f"- Comma separated\n"
    f"- No explanations\n"
    f"- No introductory text\n"
    f"- No sentences\n"
    )
    raw =  call_groq(prompt)
    return clean_ai_output(raw)
    
def clean_ai_output(text):
    bad_starts = (
        "here",
        "below",
        "this",
        "as",
        "sure",
        "following",
    )
    lines = text.strip().splitlines()
    cleaned = [
        line for line in lines
        if not line.lower().startswith(bad_starts)
    ]
    return "\n".join(cleaned).strip()
