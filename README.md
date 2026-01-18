# 임시팀장 가이드 (Interim Team Leader Guide)

작년 임시팀장직을 수행하며 경험하고 느꼈던 소중한 기록들을 공유하고 관리하기 위한 웹 애플리케이션입니다.

## 🚀 주요 기능
- **가이드 문서 조회**: 로컬 마크다운(.md) 파일을 기반으로 한 가이드 열람
- **현장 지도 상황판**: OpenLayers를 활용한 프로젝트 현장 위치 시각화
- **실시간 동기화**: 마크다운 파일 수정 시 즉시 DB(H2)와 동기화
- **API 문서화**: Swagger(OpenAPI)를 통한 백엔드 API 명세 제공

## 🛠 기술 스택
### Backend
- **Framework**: Spring Boot 3.x
- **Language**: Java 17
- **Database**: H2 Database (In-memory)
- **Documentation**: SpringDoc OpenAPI (Swagger 3)
- **Library**: Spring Data JPA, Lombok

### Frontend
- **Framework**: React (Vite)
- **Styling**: Tailwind CSS
- **Maps**: OpenLayers
- **Icons**: Lucide React
- **Markdown**: React Markdown

## 🏃 실행 방법

### 통합 실행 (권장)
루트 폴더에서 아래 명령어를 실행하면 백엔드와 프론트엔드가 동시에 시작됩니다.
```bash
./run.sh
```

### 개별 실행 (디버깅 시)
#### Backend 실행
```bash
cd backend
./mvnw spring-boot:run
```
- API Endpoint: `http://localhost:8080/api/guides`
- Swagger UI: `http://localhost:8080/swagger-ui/index.html`

#### Frontend 실행
```bash
cd frontend
npm install
npm run dev
```
- UI Address: `http://localhost:5173` (또는 터미널에 표시된 포트)

## 📁 디렉토리 구조
- `/backend`: Spring Boot 소스 코드
- `/frontend`: React 소스 코드
- `/*.md`: 실제 가이드 마크다운 파일들
