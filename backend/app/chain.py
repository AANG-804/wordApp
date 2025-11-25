import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.models import WordDefinition

# System prompt for IT/CS terminology dictionary
SYSTEM_PROMPT = """
[ROLE]
너는 전문 영어 사전이다.

[OUTPUT REQUIREMENTS]
다음 필드를 모두 정확히 제공해야 한다:
- word: 조회된 용어 (영어 그대로)
- pronunciation_ipa: IPA 발음 기호
- pronunciation_kr: 한글 발음 표기
- meaning: 간결한 뜻, 여러 의미가 있으면 콤마(,) 로 구분
- examples: 영어 예문 리스트, 각 예문은 문자열 하나씩 (예: ["Sentence 1.", "Sentence 2."])

[GUIDELINES]
1. **뜻(meaning)**: 간결한 한국어 뜻, 필요 시 콤마로 다중 의미 구분. (예: "뜻1, 뜻2, 뜻3")
2. **발음**: IPA와 한글 발음 정확히 표기
3. **예문(examples)**: 실무/학술 맥락에 맞는 영어 예문을 정확히 2개 제공, 한국어 번역은 제외
4. **다의어 처리**: 여러 의미가 있으면 가장 관련성 높은 의미를 우선하고, 나머지는 콤마로 나열
5. **맥락 중심**: 정보 시스템/컴퓨터 과학 분야 맥락에 집중
"""

def get_chain():
    llm = ChatOpenAI(model="gpt-4.1-mini")
    structured_llm = llm.with_structured_output(WordDefinition)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Define the term: {word}")
    ])
    
    chain = prompt | structured_llm
    return chain

# System prompt for Word Extraction
EXTRACTION_SYSTEM_PROMPT = """
[ROLE]
You are a helpful assistant that extracts the target English word from a user's prompt.

[OBJECTIVE]
1. Identify the core English word the user wants to define.
2. If there is a typo, correct it to the most likely intended English word.
3. If the input is invalid (random characters, not English, etc.) or cannot be corrected to a valid English word, return "INVALID".

[OUTPUT FORMAT]
Return ONLY the extracted/corrected word or "INVALID". Do not add any punctuation or explanation.
"""

def get_extraction_chain():
    llm = ChatOpenAI(model="gpt-5-nano")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", EXTRACTION_SYSTEM_PROMPT),
        ("human", "{input}")
    ])
    
    # We want a simple string output, so StrOutputParser is useful, 
    # but here we can just rely on the default message content or add a parser.
    # Let's use a simple chain that returns the content.
    from langchain_core.output_parsers import StrOutputParser
    
    chain = prompt | llm | StrOutputParser()
    return chain
