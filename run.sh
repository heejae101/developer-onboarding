#!/bin/bash

# 프로젝트 루트 경로 확보
BASE_PATH=$(pwd)

echo "🚀 임시팀장 가이드 프로젝트를 시작합니다..."

# 포트 8080(백엔드) 및 5173-5175(프론트엔드 예상 포트) 확인 및 정리
echo "🧹 기존 프로세스 확인 및 정리 중..."
kill $(lsof -t -i:8080) 2>/dev/null || true
kill $(lsof -t -i:5173-5175) 2>/dev/null || true

# 백엔드 실행
echo "📦 백엔드(Spring Boot) 실행 중..."
cd "$BASE_PATH/backend"
./mvnw spring-boot:run > "$BASE_PATH/backend.log" 2>&1 &
BACKEND_PID=$!

# 백엔드 준비 대기 (간단한 체크)
echo "⏳ 백엔드 준비 대기 중 (약 10초)..."
sleep 10

# 프론트엔드 실행
echo "🎨 프론트엔드(React/Vite) 실행 중..."
cd "$BASE_PATH/frontend"
npm run dev &
FRONTEND_PID=$!

echo "✅ 모든 서비스가 실행되었습니다!"
echo "------------------------------------------------"
echo "🌐 API & Swagger: http://localhost:8080/swagger-ui/index.html"
echo "🌐 Frontend: http://localhost:5173 (또는 표시된 포트)"
echo "------------------------------------------------"
echo "💡 중단하시려면 Ctrl+C를 누르세요."

# 자식 프로세스들이 종료될 때까지 대기 및 정리 로직
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM EXIT
wait
