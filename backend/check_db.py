import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

def check_db():
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID")
    
    # Normalize database ID
    db_id = db_id.replace("-", "")
    
    print(f"Checking Database ID: {db_id}")
    
    client = Client(auth=token)
    try:
        db = client.databases.retrieve(database_id=db_id)
        print("Success! Database found.")
        print(f"Title: {db['title'][0]['plain_text'] if db['title'] else 'Untitled'}")
    except Exception as e:
        print(f"Error retrieving database: {e}")

if __name__ == "__main__":
    check_db()
