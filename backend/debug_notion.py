import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

def debug_notion():
    token = os.getenv("NOTION_TOKEN")
    if not token:
        print("Error: NOTION_TOKEN not found in .env")
        return

    client = Client(auth=token)
    try:
        print("Searching for accessible resources...")
        results = client.search()
        
        if not results["results"]:
            print("No accessible resources found. Please ensure the integration is connected to the page/database.")
            return

        print(f"Found {len(results['results'])} resources:")
        for item in results["results"]:
            obj_type = item["object"]
            title = "Untitled"
            if obj_type == "database":
                if "title" in item and item["title"]:
                    title = item["title"][0]["plain_text"]
            elif obj_type == "page":
                if "properties" in item:
                    # Try to find a title property
                    for prop in item["properties"].values():
                        if prop["type"] == "title" and prop["title"]:
                            title = prop["title"][0]["plain_text"]
                            break
            
            print(f"- [{obj_type}] {title} (ID: {item['id']})")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_notion()
