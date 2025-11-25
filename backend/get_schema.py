import os
import json
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

def get_schema():
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID").replace("-", "")
    
    client = Client(auth=token)
    try:
        # Search for pages in the database
        results = client.search(
            query="",
            filter={"property": "object", "value": "page"},
            page_size=10
        )
        
        if results["results"]:
            # Find a page that belongs to our database
            for page in results["results"]:
                if page.get("parent", {}).get("type") == "database_id":
                    parent_id = page["parent"]["database_id"].replace("-", "")
                    if parent_id == db_id:
                        print(f"Found page in database: {page.get('id')}")
                        print("Properties:")
                        print(json.dumps(page["properties"], indent=2, ensure_ascii=False))
                        return
            
            print("No pages found in the target database")
        else:
            print("No pages found")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_schema()
