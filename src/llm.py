import os, time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"),
                      http_options={"timeout": 30000})
MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemma-4-31b-it",
          "gemma-4-26b-a4b-it", "gemini-3.8-flash", "gemini-3.5-flash",
          "gemini-3.6-flash", "gemini-3.7-flash"]

def ask(contents, config=None, tries=2):
    last = None
    for model in MODELS:
        for i in range(tries):
            print(f"... trying {model} (try {i+1})", flush=True)
            try:
                r = client.models.generate_content(model=model, contents=contents, config=config)
                print(f"[ok model={model}]", flush=True)
                return r.text
            except Exception as e:
                last = e
                print(f"    failed: {str(e)[:100]}", flush=True)
                time.sleep(2)
    raise last
