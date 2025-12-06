import os
import httpx
from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/jay/dev/blogs/wordApp/backend/.env")

def test_httpx_query():
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID")
    # Try with dashes first
    
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    body = {
        "filter": {
            "property": "단어",
            "title": {
                "equals": "test_duplicate_word"
            }
        }
    }
    
    print(f"Querying {url}...")
    try:
        response = httpx.post(url, headers=headers, json=body)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_httpx_query()
