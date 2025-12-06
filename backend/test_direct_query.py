import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/jay/dev/blogs/wordApp/backend/.env")

def test_direct_query():
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID")
    # db_id = db_id.replace("-", "")
    
    client = Client(auth=token)
    
    print(f"Querying database {db_id} using direct request...")
    
    try:
        response = client.request(
            path=f"/databases/{db_id}/query",
            method="POST",
            body={
                "filter": {
                    "property": "단어",
                    "title": {
                        "equals": "test_duplicate_word"
                    }
                }
            }
        )
        print("Success!")
        print(f"Results count: {len(response.get('results', []))}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_direct_query()
