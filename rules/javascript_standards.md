# JavaScript 개발 표준

JSP와 같은 특정 서버 사이드 템플릿 엔진에 의존하지 않는, 순수 바닐라 JavaScript 기반의 프론트엔드 개발 가이드라인입니다.

## 1. 기본 원칙
- **가독성 우선**: 이해하기 쉬운 코드 작성
- **보안 강화**: XSS, CSRF 등 웹 보안 취약점 방지
- **최소 의존성**: 필요한 라이브러리만 사용
- **모듈화**: 기능별 코드 분리로 관리 용이성 확보

## 2. 명명 규칙 (Naming Conventions)

| 구분 | 규칙 | 예시 |
| :--- | :--- | :--- |
| **변수** | camelCase | `guideList`, `searchKeyword` |
| **상수** | UPPER_SNAKE_CASE | `API_BASE_URL`, `MAX_RETRIES` |
| **함수** | 동사 + camelCase | `validateForm`, `getGuideList` |
| **Boolean** | is/has + camelCase | `isLoading`, `hasPermission` |

### 함수 명명 패턴
- **조회**: `select...`, `get...`
- **입력/수정/삭제**: `insert...`, `update...`, `delete...`
- **이벤트 핸들러**: `on...` (예: `onSubmitForm`, `onClickDelete`)

## 3. 코딩 표준

### 3.1 변수 선언
- `const`를 우선적으로 사용하고, 재할당이 필요한 경우에만 `let`을 사용합니다.
- `var`는 절대 사용하지 않습니다.

### 3.2 함수 정의
- 최상위 함수는 명확한 의미를 전달하기 위해 **함수 선언문** 형식을 권장합니다.
- 익명 함수나 콜백 함수인 경우 **화살표 함수(Arrow Function)**를 사용합니다.

### 3.3 객체 및 배열
- 리터럴 형식을 사용하여 선언합니다. (`const obj = {};`, `const arr = [];`)

## 4. DOM 조작 및 이벤트 처리

### 4.1 DOM 접근 및 스타일 제어
- `document.querySelector` 및 `document.querySelectorAll`을 사용하여 요소를 선택합니다.
- `innerHTML` 대신 `textContent`를 사용하여 XSS 공격을 방지합니다. 부득이하게 HTML을 주입해야 할 경우 반드시 이스케이프 처리를 거칩니다.
- **인라인 스타일 금지**: 자바스크립트에서 직접 스타일을 지정(`element.style.color = 'red'`)하지 않습니다. 반드시 CSS 클래스를 정의하고 `element.classList`를 사용하여 제어합니다.

### 4.2 이벤트 리스너
- `onclick` 속성 대신 `addEventListener`를 사용하여 이벤트를 바인딩합니다.
- **구체적인 이벤트 타겟 지정**: `document.addEventListener`와 같이 전체 문서에 이벤트를 거는 것을 지양합니다. 반드시 필요한 특정 요소나 컨테이너를 타겟으로 지정합니다.
- 동적으로 생성되는 요소에 대해서는 **이벤트 위임(Event Delegation)** 패턴을 활용하되, 위임 대상 역시 최소한의 범위를 가진 부모 요소를 선택합니다.

## 5. 비동기 통신 (AJAX)
- `XMLHttpRequest` 대신 브라우저 표준인 **Fetch API**를 사용합니다.
- `Promise` 체이닝보다는 `async/await` 문법을 사용하여 가독성을 높입니다.

## 6. 보안 및 유효성 검사
- 모든 사용자 입력값은 서버 전송 전 프론트엔드에서 1차 검증(Validation)을 수행합니다.
- 외부 데이터를 화면에 출력할 때 반드시 **Security.escapeHtml**과 같은 방어 로직을 적용합니다.

## 7. 주석 작성
- **Why(왜)** 이 코드가 필요한지에 집중하여 작성합니다.
- 복잡한 로직이나 공통 모듈의 경우 JSDoc 스타일의 주석을 사용하여 파라미터와 반환값을 명시합니다.
