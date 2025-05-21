import os
from ocr import extract_text_from_image
from vector import store_conversation
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def suggest_reply(screenshot_text, user_draft, notion_prompts):
    system_prompt = f"""
You are a network marketing assistant helping improve client conversations.
Refer to these reply principles:
{notion_prompts}
"""
    user_input = f"""
Client Screenshot Text:
{screenshot_text}

User Draft:
{user_draft}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    # Placeholder for demonstration
    text = extract_text_from_image("example_screenshot.png")
    draft = "Hey! Just thought I’d check in and see how you’re going with everything!"
    notion_frameworks = "Start with curiosity. Avoid pitching early. Ask about their goals or energy lately."

    reply = suggest_reply(text, draft, notion_frameworks)
    print("Suggested Final Reply:", reply)
    store_conversation(text, draft, reply)