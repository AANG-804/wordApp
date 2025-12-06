import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from app.models import LookupRequest, SaveRequest, WordDefinition
from app.chain import get_chain, get_extraction_chain
from app.notion_client import add_word_to_database

from pathlib import Path

# 현재 파일(main.py)의 상위 폴더 → /backend
BASE_DIR = Path(__file__).resolve().parent.parent

# /backend/.env 경로
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

# LangSmith Tracing Configuration
os.environ['LANGSMITH_TRACING'] = 'true'
os.environ['LANGSMITH_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGSMITH_PROJECT'] = 'WordApp'
# LANGSMITH_API_KEY is expected to be in the loaded .env file

app = FastAPI(title="WordApp API")

@app.post("/lookup", response_model=WordDefinition)
async def lookup_word(request: LookupRequest):
    try:
        # 1. Extract/Validate the word
        extraction_chain = get_extraction_chain()
        extracted_word = extraction_chain.invoke({"input": request.word})
        
        if extracted_word.strip() == "INVALID":
             raise HTTPException(status_code=400, detail="Invalid prompt. Please enter a valid English word.")
        
        # 2. Get Definition for the extracted word
        chain = get_chain()
        result = chain.invoke({"word": extracted_word})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save")
async def save_word(request: SaveRequest):
    try:
        await add_word_to_database(request.definition)
        return {"status": "success", "message": "Saved to Notion"}
    except ValueError as e:
        if str(e) == "Duplicate word":
             raise HTTPException(status_code=409, detail="Word already exists in Notion")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
