import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

def test_create():
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID").replace("-", "")
    
    client = Client(auth=token)
    
    # Test with just  the minimal required properties
    test_properties = [
        # Try 1: No title key (use first available)
        {},
        # Try 2: Common English names
        {"Title": {"title": [{"text": {"content": "Test"}}]}},
        {"title": {"title": [{"text": {"content": "Test"}}]}},
        # Try 3: Empty string as key
        {"": {"title": [{"text": {"content": "Test"}}]}},
    ]
    
    for i, props in enumerate(test_properties, 1):
        try:
            print(f"\nAttempt {i}: {list(props.keys()) if props else 'empty'}")
            response = client.pages.create(
                parent={"database_id": db_id},
                properties=props if props else {"title": [{"text": {"content": "Test"}}]}
            )
            print(f"SUCCESS! Title property is: {list(props.keys())[0] if props else 'default'}")
            print(f"Page ID: {response['id']}")
            # Delete the test page
            client.pages.update(page_id=response['id'], archived=True)
            break
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    test_create()
