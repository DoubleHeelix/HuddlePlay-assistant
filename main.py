import os
from ocr import extract_text_from_image
from vector import store_conversation
import openai
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")

def fetch_notion_training():
    results = notion.databases.query(database_id=database_id)
    training_texts = []
    for page in results['results']:
        props = page['properties']
        title = props['Name']['title'][0]['plain_text'] if props['Name']['title'] else ""
        content = props['Content']['rich_text'][0]['plain_text'] if props['Content']['rich_text'] else ""
        training_texts.append(f"{title}: {content}")
    return "\\n".join(training_texts)

def suggest_reply(screenshot_text, user_draft):
    notion_prompts = fetch_notion_training()  # Fetch live Notion data here

    system_prompt = f\"\"\"
You are a network marketing assistant helping improve client conversations.
Refer to these reply principles:
{notion_prompts}
\"\"\"
    user_input = f\"\"\"
Client Screenshot Text:
{screenshot_text}

User Draft:
{user_draft}
\"\"\"
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    text = extract_text_from_image("example_screenshot.png")
    draft = "Hey! Just thought I’d check in and see how you’re going with everything!"

    reply = suggest_reply(text, draft)
    print("Suggested Final Reply:", reply)
    store_conversation(text, draft, reply)
