# Xcode 프로젝트 생성 가이드

## 준비된 파일들
- `WordApp/WordApp/WordApp.swift` - 앱 엔트리 포인트
- `WordApp/WordApp/ContentView.swift` - 메인 UI
- `WordApp/WordApp/NetworkManager.swift` - API 통신

## Xcode 프로젝트 생성 방법

### 1. Xcode 실행
터미널에서:
```bash
open -a Xcode
```

### 2. 새 프로젝트 생성
1. "Create New Project" 선택
2. "macOS" 탭 → "App" 템플릿 선택
3. Next 클릭

### 3. 프로젝트 설정
- **Product Name**: `WordApp`
- **Team**: 본인 계정 선택
- **Organization Identifier**: `com.yourname` (아무거나)
- **Interface**: `SwiftUI`
- **Language**: `Swift`
- **Storage**: `None`

### 4. 저장 위치
`/Users/jay/dev/blogs/wordApp/` 폴더에 저장
(기존 `WordApp` 폴더와 병합하거나 새 이름으로 생성)

### 5. 파일 교체
Xcode 프로젝트가 생성되면:
1. 좌측 네비게이터에서 기본 생성된 파일들 확인
2. `WordAppApp.swift` 내용을 → `WordApp/WordApp/WordApp.swift` 내용으로 교체
3. `ContentView.swift` 내용을 → `WordApp/WordApp/ContentView.swift` 내용으로 교체
4. `NetworkManager.swift` 파일 추가:
   - 프로젝트 네비게이터에서 우클릭 → "New File"
   - "Swift File" 선택
   - 이름: `NetworkManager`
   - 내용을 `WordApp/WordApp/NetworkManager.swift`에서 복사

### 6. App Sandbox 설정
1. 프로젝트 네비게이터에서 프로젝트 이름 클릭 (최상위)
2. "Signing & Capabilities" 탭
3. "App Sandbox" 섹션에서:
   - ✅ "Outgoing Connections (Client)" 체크

### 7. 빌드 및 실행
- `Cmd + R` 또는 상단의 재생 버튼 클릭
- 백엔드가 `http://localhost:8000`에서 실행 중인지 확인

## 트러블슈팅

### 백엔드가 실행 중이 아닌 경우:
```bash
cd /Users/jay/dev/blogs/wordApp/backend
docker start wordapp
# 또는
docker run -d -p 8000:8000 --env-file .env --name wordapp wordapp-backend
```

### 네트워크 연결 오류:
- App Sandbox 설정 확인
- 백엔드 health check: `curl http://localhost:8000/health`
