# [상세 설계] API 및 인터페이스 설계

## 1. 서비스 간 통신 구조
1. **Frontend <--> Java Backend**: REST API (HTTP/JSON)
2. **Java Backend <--> Python MCP Server**: JSON-RPC over MCP
3. **Python MCP Server <--> LLM**: OpenAI / Anthropic SDK

---

## 2. 주요 API 명세 (Java Backend)

### 2.1 일일 업무 관리
- `GET /api/v1/work`: 오늘 또는 특정 날짜의 업무 리스트 조회.
- `POST /api/v1/work`: 새 업무 기록 추가.
- `PATCH /api/v1/work/{id}`: 업무 상태(완료 등) 변경.

### 2.2 AI 에이전트 채팅
- `POST /api/v1/ai/chat`: 사용자의 질문을 에이전트에 전달.
  - **Request**: `{ "message": "Java 컨벤션 알려줘", "context": "PRACTICE" }`
  - **Internal Process**: Java 서버가 Python MCP 에이전트의 랭그래프 호출.

---

## 3. MCP 인터페이스 설계 (Java <-> Python)

### 3.1 Tools 정의 (Python side)
- `search_rules(query)`: 질문에 맞는 프로젝트 룰 검색.
- `verify_code(code)`: 제출된 코드가 룰에 맞는지 검사.
- `execute_workflow(trigger)`: 특정 자동화 워크플로우 실행.

### 3.2 Resources 정의
- `resource://rules/main`: 현재 적용 중인 `rules.md` 원본 노출.

---

## 4. 데이터 교환 포맷
- 모든 통신은 UTF-8 기반 JSON을 사용하며, 날짜 형식은 ISO-8601(`YYYY-MM-DDTHH:mm:ssZ`)을 준수합니다.
