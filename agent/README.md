# Onboarding Agent Service

LangGraph 기반 FastAPI 에이전트 서비스. 이 문서는 에이전트를 단독으로 실행하는 방법에 집중합니다.

## Overview
- FastAPI 앱 엔트리: `src/main.py`
- REST API: `/api/v1/*`
- WebSocket: `/ws/ai-stream`
- 기본 포트: `8000`

## Requirements
- Python 3.11
- Poetry

## Install
```bash
cd agent
poetry install
```

## Environment
```bash
cp .env.example .env
```

### API 모드 (기본값)
```env
LLM_MODE=api
LLM_PROVIDER=openai  # 또는 anthropic
OPENAI_API_KEY=sk-...
```

### 로컬 모드 (Ollama)
```env
LLM_MODE=local
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3
```

## Run
```bash
poetry run uvicorn src.main:app --reload --port 8000
```

## Verify
```bash
curl http://localhost:8000/api/v1/health
```

## API Endpoints
| Method | Endpoint | 설명 |
| --- | --- | --- |
| GET | `/api/v1/health` | 헬스체크 |
| POST | `/api/v1/chat` | AI 채팅 |
| POST | `/api/v1/code-review` | 코드 리뷰 |
| POST | `/api/v1/agent/task` | 자율 에이전트 태스크 |

### 예시: 채팅
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "API 규칙 알려줘"}'
```

### 예시: 코드 리뷰
```bash
curl -X POST http://localhost:8000/api/v1/code-review \
  -H "Content-Type: application/json" \
  -d '{"code": "@RestController\npublic class UserController {}", "language": "java"}'
```

## Admin Endpoints
| Method | Endpoint | 설명 |
| --- | --- | --- |
| GET | `/api/admin/graph-settings` | 그래프 설정 조회 |
| PUT | `/api/admin/graph-settings` | 그래프 설정 업데이트 |
| GET | `/api/admin/graph-visualization` | 그래프 시각화 정보 |

## Graph Settings
그래프 토글은 `src/graph_settings.py`와 `src/graph_settings.json`에서 관리합니다.

주요 설정 키:
- `enable_self_rag`: 검색 결과 평가 후 재검색 여부
- `enable_parallel_search`: RAG와 파일 검색 병렬 실행
- `enable_answer_grading`: 답변 품질 평가 및 개선 루프
- `enable_human_approval`: 중요 결정에 사용자 확인
- `enable_step_logging`: 노드 실행 로그 출력

## Tests
```bash
poetry run pytest
```

## Project Structure
```
agent/
├── pyproject.toml      # Poetry 설정
├── .env.example        # 환경 변수 템플릿
├── README.md
└── src/
    ├── main.py         # FastAPI 앱 엔트리포인트
    ├── config.py       # 설정 관리
    ├── llm/            # LLM 클라이언트
    │   ├── __init__.py
    │   └── client.py   # OpenAI/Anthropic/Ollama 클라이언트
    ├── agent/          # LangGraph 에이전트
    │   ├── __init__.py
    │   ├── state.py    # AgentState 정의
    │   ├── nodes.py    # 노드 구현
    │   └── graph.py    # 그래프 빌더
    └── api/            # FastAPI 라우터
        ├── __init__.py
        ├── routes.py   # API 엔드포인트
        └── schemas.py  # Pydantic 스키마
```

## Troubleshooting
- 포트 8000 사용 중: 다른 프로세스를 종료하거나 포트를 변경하세요.
- API 모드에서 키 누락: `OPENAI_API_KEY` 또는 `ANTHROPIC_API_KEY`를 설정하세요.
- 로컬 모드 실패: Ollama가 실행 중인지 확인하고 `OLLAMA_MODEL`을 점검하세요.
- RAG 초기화 실패: 로그를 확인하고 환경 변수 설정을 재확인하세요.
