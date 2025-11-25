from typing import List
from pydantic import BaseModel, Field

class WordDefinition(BaseModel):
    """Model for term definition used by the LLM chain.
    - `word`: original English term
    - `meaning`: concise academic/MIS definition; multiple senses separated by commas
    - `examples`: list of English example sentences, each on its own line in the output
    """
    word: str = Field(description="The word being defined")
    pronunciation_ipa: str = Field(description="IPA pronunciation")
    pronunciation_kr: str = Field(description="Korean pronunciation")
    meaning: str = Field(description="Concise definition in korean; multiple meanings separated by commas (예: \"뜻1, 뜻2, 뜻3\")")
    examples: List[str] = Field(description="English example sentences, one per list entry")

class LookupRequest(BaseModel):
    word: str

class SaveRequest(BaseModel):
    definition: WordDefinition
