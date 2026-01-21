#!/bin/bash

# 프로젝트 루트 경로 확보
BASE_PATH=$(pwd)

echo "🚀 임시팀장 가이드 프로젝트를 시작합니다..."

# 포트 확인 및 정리
echo "🧹 기존 프로세스 확인 및 정리 중..."
kill $(lsof -t -i:8080) 2>/dev/null || true
kill $(lsof -t -i:8000) 2>/dev/null || true
kill $(lsof -t -i:5173-5175) 2>/dev/null || true

# 백엔드(Spring Boot) 실행
echo "📦 백엔드(Spring Boot) 실행 중..."
cd "$BASE_PATH/backend"
./mvnw spring-boot:run | tee "$BASE_PATH/backend.log" &
BACKEND_PID=$!

# 백엔드 준비 대기
echo "⏳ 백엔드 준비 대기 중 (약 10초)..."
sleep 10

# AI 에이전트(FastAPI) 실행
echo "🤖 AI 에이전트(FastAPI) 실행 중..."
cd "$BASE_PATH/agent"
if [ -d ".venv" ]; then
    source .venv/bin/activate
    uvicorn src.main:app --reload --port 8000 | tee "$BASE_PATH/agent.log" &
elif command -v poetry &> /dev/null; then
    poetry run uvicorn src.main:app --reload --port 8000 | tee "$BASE_PATH/agent.log" &
else
    echo "⚠️  Poetry가 설치되어 있지 않습니다. agent 서비스 스킵..."
fi
AGENT_PID=$!

# 에이전트 준비 대기
sleep 3

# 프론트엔드(React/Vite) 실행
echo "🎨 프론트엔드(React/Vite) 실행 중..."
cd "$BASE_PATH/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ 모든 서비스가 실행되었습니다!"
echo "------------------------------------------------"
echo "🌐 Spring Backend:  http://localhost:8080"
echo "🌐 Swagger UI:      http://localhost:8080/swagger-ui/index.html"
echo "🤖 AI Agent API:    http://localhost:8000"
echo "🤖 Agent Docs:      http://localhost:8000/docs"
echo "🎨 Frontend:        http://localhost:5173"
echo "------------------------------------------------"
echo "💡 중단하시려면 Ctrl+C를 누르세요."

# 자식 프로세스들이 종료될 때까지 대기 및 정리 로직
trap "kill $BACKEND_PID $AGENT_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM EXIT
wait
