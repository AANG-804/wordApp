import os
import json
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

def inspect_db():
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID")
    
    client = Client(auth=token)
    try:
        db = client.databases.retrieve(database_id=db_id)
        print(f"Retrieved object type: {db['object']}")
        
        if "properties" in db:
            print("Database Properties:")
            print(json.dumps(db["properties"], indent=2, ensure_ascii=False))
        else:
            print("No properties found in response.")
            print(json.dumps(db, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error retrieving database: {e}")

if __name__ == "__main__":
    inspect_db()
