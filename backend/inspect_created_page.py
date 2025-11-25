import os
import json
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

def inspect_created_page():
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID").replace("-", "")
    
    client = Client(auth=token)
    
    # Create minimal page first
    try:
        print("Creating minimal test page...")
        response = client.pages.create(
            parent={"database_id": db_id},
            properties={}
        )
        page_id = response['id']
        print(f"Created page: {page_id}")
        
        # Now retrieve it to see the structure
        print("\nRetrieving page to see properties...")
        page = client.pages.retrieve(page_id=page_id)
        print(json.dumps(page["properties"], indent=2, ensure_ascii=False))
        
        # Clean up
        print(f"\nArchiving test page...")
        client.pages.update(page_id=page_id, archived=True)
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_created_page()
