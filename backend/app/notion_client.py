import os
from notion_client import Client
from app.models import WordDefinition

def get_notion_client():
    token = os.getenv("NOTION_TOKEN")
    if not token:
        raise ValueError("NOTION_TOKEN is not set")
    return Client(auth=token)

import httpx

async def check_word_exists(word: str) -> bool:
    token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    if not database_id:
        raise ValueError("NOTION_DATABASE_ID is not set")
    
    database_id = database_id.replace("-", "")
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json={
                "filter": {
                    "property": "단어",
                    "title": {
                        "equals": word
                    }
                }
            }
        )
        
    if response.status_code != 200:
        # Fallback or log error? For now, assume no duplicate if error, or raise?
        # Raising is safer to prevent duplicates if API fails.
        raise ValueError(f"Failed to check Notion: {response.text}")
        
    data = response.json()
    return len(data.get("results", [])) > 0

async def add_word_to_database(data: WordDefinition):
    # Check for duplicates first
    if await check_word_exists(data.word):
        raise ValueError("Duplicate word")

    notion = get_notion_client()
    database_id = os.getenv("NOTION_DATABASE_ID")
    if not database_id:
        raise ValueError("NOTION_DATABASE_ID is not set")
    
    # Normalize database ID by removing hyphens
    database_id = database_id.replace("-", "")

    # Format examples as a single string for the text property
    examples_text = ""
    for i, ex in enumerate(data.examples, 1):
        examples_text += f"{i}. {ex}\n"

    # Build properties - use actual database schema discovered via API
    properties = {
        "단어": {"title": [{"text": {"content": data.word}}]},  # Title property is named "단어"
        "발음": {"rich_text": [{"text": {"content": f"{data.pronunciation_ipa} / {data.pronunciation_kr}"}}]},
        "단어 뜻": {"rich_text": [{"text": {"content": data.meaning}}]},
        "예문": {"rich_text": [{"text": {"content": examples_text}}]},
        "상태": {"status": {"name": "학습 전"}}
    }

    response = notion.pages.create(
        parent={"database_id": database_id},
        properties=properties
    )
    return response
