import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

def list_databases():
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    
    try:
        print("Searching for accessible resources...")
        results = client.search()
        
        if not results["results"]:
            print("No accessible databases found.")
            print("\nSearching for all resources...")
            all_results = client.search()
            print(f"Total accessible resources: {len(all_results['results'])}")
            for item in all_results["results"]:
                print(f"- [{item['object']}] ID: {item['id']}")
            return

        print(f"Found {len(results['results'])} database(s):")
        for db in results["results"]:
            title = "Untitled"
            if "title" in db and db["title"]:
                title = db["title"][0]["plain_text"]
            print(f"- {title} (ID: {db['id']})")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_databases()
