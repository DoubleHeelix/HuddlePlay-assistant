import json
import uuid
from openai import OpenAI
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def store_conversation(screenshot_text, user_draft, final_reply):
    # Save a vector-like memory entry locally
    record = {
        "id": str(uuid.uuid4()),
        "screenshot_text": screenshot_text,
        "user_draft": user_draft,
        "final_reply": final_reply
    }
    with open("memory.json", "a") as f:
        f.write(json.dumps(record) + "\n")