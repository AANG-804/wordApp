# WordApp

새로운 단어를 관리하고 학습하는 데 도움을 주기 위해 설계된 개인용 단어장 애플리케이션입니다. 이 프로젝트는 새로운 어휘를 기록하고 복습하는 과정을 간소화하기 위해 개인적인 용도로 개발되었습니다.  
<p align="center">
  <img src="https://github.com/user-attachments/assets/2dcee3c7-d4ea-4c20-a348-ae90a3642598" alt="image" width="715" height="611" />
</p>

### 주요 기능
1. 프롬프트 필터링:사용자의 입력(영어 단어 검색)에서 영어 단어/구를 필터링합니다. 간단한 오타는 자동으로 수정하고, invalid input을 입력한 경우에는 에러 메세지를 반환합니다.
2. 구조화된 출력: 영어 단어 검색 결과를 발음 기호, 발음, 예문으로 구조화해서 출력합니다.
3. 히스토리 기능: 영어 단어 검색 결과는 카드로 저장되며, 히스토리가 남기 때문에 이전 검색 결과를 열람할 수 있습니다.
4. Notion 데이터베이스 연동: 검색 결과를 즉시 Notion 데이터베이스에 저장할 수 있습니다. (Notion 데이터베이스를 이용해 단어장을 생성하고 학습할 수 있습니다. / 추후 Notion 템플릿 공유 예정)

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
