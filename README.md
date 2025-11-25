# WordApp

새로운 단어를 관리하고 학습하는 데 도움을 주기 위해 설계된 개인용 단어장 애플리케이션입니다. 이 프로젝트는 새로운 어휘를 기록하고 복습하는 과정을 간소화하기 위해 개인적인 용도로 개발되었습니다.

**[Antigravity](https://github.com/google-deepmind/antigravity)** (Agentic AI Coding Assistant)를 사용하여 개발되었습니다.

## 주요 기능 (Features)

- **macOS 네이티브 앱**: SwiftUI로 구축된 깔끔한 네이티브 macOS 인터페이스를 제공합니다.
- **Notion 연동**: 정의된 단어를 Notion 데이터베이스에 자동으로 저장하여 쉽게 복습하고 추적할 수 있습니다.
- **AI 기반 정의**: LLM(대규모 언어 모델)을 사용하여 정확한 정의와 예문을 제공합니다.
- **영어 단어 추출**: 사용자 입력에서 영어 단어를 자동으로 감지 및 추출하며, 오타를 수정하고 유효하지 않은 입력을 필터링합니다.
- **검색 기록**: 검색된 단어들의 세션 기반 기록을 유지합니다.
- **Dockerized 백엔드**: 백엔드는 컨테이너화되어 있어 일관된 배포와 쉬운 설정이 가능합니다.

## 기술 스택 (Tech Stack)

- **Frontend**: Swift (SwiftUI)
- **Backend**: Python (FastAPI)
- **Database**: Notion (via API)
- **AI**: LangChain, OpenAI GPT
- **Deployment**: Docker

## 시작하기 (Getting Started)

### 필수 조건 (Prerequisites)

- Docker
- Xcode (macOS 앱용)
- Notion Integration Token 및 Database ID
- OpenAI API Key

### 백엔드 설정 (Backend Setup)

1. 레포지토리를 클론합니다.
2. `backend/` 디렉토리에 `.env` 파일을 생성하고 API 키를 입력합니다:
    ```env
    OPENAI_API_KEY=your_key
    NOTION_TOKEN=your_token
    NOTION_DATABASE_ID=your_db_id
    LANGSMITH_API_KEY=your_langsmith_key (선택 사항)
    ```
3. Docker로 실행합니다:
    ```bash
    docker-compose up --build
    ```

### 프론트엔드 설정 (Frontend Setup)

1. Xcode에서 `WordApp/WordApp.xcodeproj`를 엽니다.
2. 애플리케이션을 빌드하고 실행합니다.
