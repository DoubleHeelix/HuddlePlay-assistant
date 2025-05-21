import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")

def fetch_notion_training():
    results = notion.databases.query(database_id=database_id)
    training_texts = []
    for page in results['results']:
        props = page['properties']
        # Replace 'Name' and 'Content' with your actual column names in Notion
        title = props['Name']['title'][0]['plain_text'] if props['Name']['title'] else ""
        content = props['Content']['rich_text'][0]['plain_text'] if props['Content']['rich_text'] else ""
        training_texts.append(f"{title}: {content}")
    return "\\n".join(training_texts)

if __name__ == "__main__":
    print(fetch_notion_training())
