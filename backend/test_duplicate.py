import asyncio
import os
from app.notion_client import check_word_exists, add_word_to_database
from app.models import WordDefinition
from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/jay/dev/blogs/wordApp/backend/.env")

async def test_duplicate_check():
    # 1. Check a word that likely exists (or we can add one first)
    word = "test_duplicate_word"
    
    print(f"Checking if '{word}' exists...")
    exists = await check_word_exists(word)
    print(f"Exists: {exists}")
    
    if not exists:
        print(f"Adding '{word}' to database...")
        definition = WordDefinition(
            word=word,
            pronunciation_ipa="[test]",
            pronunciation_kr="테스트",
            meaning="A word for testing duplicates",
            examples=["This is a test."]
        )
        try:
            await add_word_to_database(definition)
            print("Added successfully.")
        except Exception as e:
            print(f"Failed to add: {e}")
            
        # Check again
        exists = await check_word_exists(word)
        print(f"Exists after add: {exists}")
        assert exists == True
        
    # 2. Try to add it again
    print(f"Trying to add '{word}' again...")
    definition = WordDefinition(
        word=word,
        pronunciation_ipa="[test]",
        pronunciation_kr="테스트",
        meaning="A word for testing duplicates",
        examples=["This is a test."]
    )
    
    try:
        await add_word_to_database(definition)
        print("Error: Should have raised ValueError")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        assert str(e) == "Duplicate word"

if __name__ == "__main__":
    asyncio.run(test_duplicate_check())
