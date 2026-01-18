---
tags:
  - JavaScript
  - 개발표준
  - 가이드라인
---

# 인천플랫폼 JavaScript 개발표준 초안

> [!NOTE] 프로젝트 개요
> JSP 기반 SSR 환경에서 순수 바닐라 JavaScript를 활용한 일관성 있는 프론트엔드 개발 가이드라인을 제시합니다.

---

## 1. 개요

### 1.1 목적
JSP 기반 SSR 환경에서 순수 바닐라 JavaScript를 활용한 일관성 있는 프론트엔드 개발 가이드라인을 제시합니다.

### 1.2 기본 원칙
- **가독성 우선**: 이해하기 쉬운 코드 작성
- **보안 강화**: XSS, CSRF 등 웹 보안 취약점 방지
	- **최소 의존성**: 필요한 라이브러리만 사용
- **모듈화**: 관리 용이성 확보
- **인라인 스타일 금지**: 유지보수를 위해 자바스크립트에서 직접적인 스타일 지정(`element.style`)을 지양합니다.

---

## 2. 파일 구조

### 2.1 디렉토리 구조

```
js/
├── common/
│   ├── common.js       # 공통 유틸리티
│   ├── validation.js   # 폼 검증
│   ├── api.js         # AJAX 통신
│   └── security.js    # 보안 관련
├── {서비스}/
│   └── {업무}/
│       └── {업무}.js  # 업무별 스크립트
└── lib/
    ├── chart.min.js   # Chart.js (권장)
    └── polyfill.js    # 브라우저 호환성 (선택적)
```

### 2.2 JSP 로드 순서 (권장)

```jsp
<!-- 1. 필요시 폴리필 로드 -->
<script src="/js/lib/polyfill.js"></script>

<!-- 2. 공통 스크립트 -->
<script src="/js/common/common.js"></script>
<script src="/js/common/validation.js"></script>
<script src="/js/common/api.js"></script>
<script src="/js/common/security.js"></script>

<!-- 3. 업무별 스크립트 -->
<script src="/js/board/boardList.js"></script>
```

---

## 3. 명명 규칙 (권장)

| 구분    | 규칙               | 예시                            |
| ------- | ------------------ | ------------------------------- |
| 변수    | camelCase          | `boardList`, `searchKeyword`    |
| 상수    | UPPER_SNAKE_CASE   | `API_BASE_URL`, `MAX_FILE_SIZE` |
| 함수    | 동사 + camelCase   | `validateForm`, `getBoardList`  |
| Boolean | is/has + camelCase | `isLoggedIn`, `hasPermission`   |

### 3.1 함수 명명 패턴 (권장)

```javascript
// CRUD 함수
function selectBoardList() {} // 조회
function insertBoard() {} // 등록
function updateBoard() {} // 수정
function deleteBoard() {} // 삭제

// 이벤트 핸들러
function onSubmitBoard() {} // 폼 제출
function onClickDelete() {} // 삭제 버튼 클릭
```

---

## 4. 코딩 표준 (권장)

### 4.1 변수 선언

```javascript
// 권장 - const 우선 사용
const boardId = 123;
const boardList = [];

// 재할당 필요시 let 사용
let currentPage = 1;
let isLoading = false;

// 사용 금지 - var
```

### 4.2 함수 선언

```javascript
// 권장 - 함수 선언문
function validateBoardForm() {
  // 구현 내용
}

// 콜백 함수는 화살표 함수 (권장)
boardList.forEach((board) => {
  console.log(board.title);
});
```

### 4.3 객체 및 배열

```javascript
// 권장 - 리터럴 사용
const boardVO = {
  title: "제목",
  content: "내용",
  writer: "작성자",
};

const searchConditions = ["title", "content", "writer"];
```

---

## 5. DOM 조작

### 5.1 기본 DOM 함수 (권장)

```javascript
// DOM 선택
const element = document.querySelector("#boardTable");
const elements = document.querySelectorAll(".btn-delete");

// 이벤트 리스너
element.addEventListener("click", onClickHandler);

// 클래스 조작 (권장)
element.classList.add("active");
element.classList.remove("disabled");
element.classList.toggle("visible");

// 인라인 스타일 사용 금지 (유지보수 저해)
// ❌ 나쁜 예: element.style.color = "red";
// ✅ 좋은 예: element.classList.add("text-error");

// 내용 변경
element.textContent = "안전한 텍스트";
element.innerHTML = sanitizedHtml;
```

### 5.2 이벤트 처리 (권장)

```javascript
// 페이지 초기화
document.addEventListener("DOMContentLoaded", function () {
  initializePage();
});

function initializePage() {
  attachEventListeners();
  loadInitialData();
}

// 이벤트 위임 활용 (권장)
// ❌ 나쁜 예: document.addEventListener('click', ...) - 전체 문서 대상 이벤트 감시는 지양
// ✅ 좋은 예: 특정 컨테이너를 지정하여 범위 제한
const tableContainer = document.getElementById("boardTable");
if (tableContainer) {
  tableContainer.addEventListener("click", function (event) {
    if (event.target.classList.contains("btn-delete")) {
      const boardId = event.target.dataset.boardId;
      deleteBoardItem(boardId);
    }
  });
}
```

---

## 6. AJAX 통신 (권장)

### 6.1 Fetch API 사용

```javascript
// common/api.js
async function callApi(options) {
  const defaults = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
    },
  };

  const config = Object.assign({}, defaults, options);

  try {
    const response = await fetch(config.url, {
      method: config.method,
      headers: config.headers,
      body: config.data ? JSON.stringify(config.data) : null,
    });

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API 호출 실패:", error);
    throw error;
  }
}

// 사용 예시
async function getBoardList(searchVO) {
  try {
    const response = await callApi({
      url: "/api/v1/board",
      method: "GET",
      data: searchVO,
    });

    return response;
  } catch (error) {
    alert("게시판 목록을 불러오는데 실패했습니다.");
    throw error;
  }
}
```

---

## 7. 폼 검증 (권장)

### 7.1 검증 함수

```javascript
// common/validation.js
const Validation = {
  required: function (element, message) {
    if (!element.value.trim()) {
      this.showError(element, message || "필수 입력사항입니다.");
      return false;
    }
    this.clearError(element);
    return true;
  },

  email: function (element, message) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (element.value.trim() && !emailPattern.test(element.value)) {
      this.showError(element, message || "올바른 이메일 형식이 아닙니다.");
      return false;
    }
    this.clearError(element);
    return true;
  },

  showError: function (element, message) {
    element.classList.add("error");

    let errorDiv = element.parentNode.querySelector(".error-message");
    if (!errorDiv) {
      errorDiv = document.createElement("div");
      errorDiv.className = "error-message";
      element.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
    element.focus();
  },

  clearError: function (element) {
    element.classList.remove("error");
    const errorDiv = element.parentNode.querySelector(".error-message");
    if (errorDiv) {
      errorDiv.remove();
    }
  },
};

// 사용 예시
function validateBoardForm() {
  const titleInput = document.getElementById("title");
  const contentInput = document.getElementById("content");

  let isValid = true;

  if (!Validation.required(titleInput, "제목을 입력해주세요.")) {
    isValid = false;
  }

  if (!Validation.required(contentInput, "내용을 입력해주세요.")) {
    isValid = false;
  }

  return isValid;
}
```

---

## 8. 보안 규칙 (권장)

### 8.1 XSS 방지

```javascript
// common/security.js
const Security = {
  escapeHtml: function (unsafe) {
    if (typeof unsafe !== "string") return unsafe;

    return unsafe
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  },

  setTextContent: function (selector, text) {
    const element = document.querySelector(selector);
    if (element) {
      element.textContent = text;
    }
  },
};

// 사용 예시
function displayBoardTitle(board) {
  // 안전한 방법
  Security.setTextContent("#boardTitle", board.title);

  // 또는 직접 사용
  document.getElementById("boardTitle").textContent = board.title;
}
```

---

## 9. 주석 가이드 (권장)

### 9.1 일반 업무 코드 주석

> [!TIP] 원칙
> 코드가 스스로 설명되도록 하되, 필요한 경우만 간단한 주석을 사용합니다.

```javascript
// 좋은 예 - 왜(Why)에 집중
function calculateTotalPrice(items, discountRate) {
  // 할인율이 50%를 초과하면 최대 50%로 제한
  const maxDiscountRate = Math.min(discountRate, 0.5);

  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal * (1 - maxDiscountRate);
}

// 좋은 예 - 복잡한 로직 설명
function processSearchKeyword(keyword) {
  // 특수문자 제거 후 SQL 인젝션 방지를 위한 이스케이프 처리
  return keyword
    .replace(/[<>'"&]/g, "")
    .trim()
    .toLowerCase();
}

// 나쁜 예 - 불필요한 주석
function getUserName() {
  return this.name; // 이름을 반환한다
}
```

### 9.2 공통/라이브러리 코드 주석

> [!TIP] 원칙
> 재사용성을 위해 JSDoc 등을 활용하여 완전한 문서화를 지향합니다.

```javascript
/**
 * 게시판 목록을 조회합니다.
 * @param {Object} searchVO - 검색 조건
 * @param {string} searchVO.searchCondition - 검색 조건 (title, content, writer)
 * @param {string} searchVO.searchKeyword - 검색 키워드
 * @param {number} searchVO.pageIndex - 페이지 번호 (기본값: 1)
 * @param {number} searchVO.pageSize - 페이지 크기 (기본값: 10)
 * @returns {Promise<Object>} API 응답 데이터
 * @throws {Error} 네트워크 오류 또는 서버 오류
 *
 * @example
 * // 기본 사용법
 * const result = await getBoardList({
 *   searchCondition: 'title',
 *   searchKeyword: '공지',
 *   pageIndex: 1
 * });
 */
async function getBoardList(searchVO) {
  // 구현 내용...
}
```

### 9.3 TODO/FIXME 및 특수 주석

```javascript
// TODO: 페이지네이션 성능 최적화 필요
function displayPagination(paginationInfo) {
  // 구현 내용...
}

// FIXME: IE11에서 fetch 폴리필 이슈 해결 필요
async function callApi(options) {
  // 구현 내용...
}

// NOTE: 이 함수는 보안상 중요하므로 수정 시 보안팀 검토 필요
function sanitizeUserInput(input) {
  // 구현 내용...
}
```

### 9.4 주석 작성 가이드라인 (요약)

| 상황               | 주석 레벨 | 예시                           |
| ------------------ | --------- | ------------------------------ |
| 일반 비즈니스 로직 | 간단      | `// 할인율 계산`               |
| 복잡한 알고리즘    | 설명      | `// 이진 탐색으로 성능 최적화` |
| 공통 유틸리티      | JSDoc     | `/** @param {string} url */`   |
| 임시 코드          | TODO      | `// TODO: 리팩토링 필요`       |
| 보안 관련          | NOTE      | `// NOTE: XSS 방지 처리`       |

---

## 10. 실제 사용 예시

### 10.1 게시판 목록 페이지 모듈 구성

```javascript
// board/boardList.js
(function () {
  "use strict";

  let currentPage = 1;

  // 페이지 초기화
  document.addEventListener("DOMContentLoaded", function () {
    attachEventListeners();
    loadBoardList();
  });

  function attachEventListeners() {
    // 검색 폼
    const searchForm = document.getElementById("searchForm");
    if (searchForm) {
      searchForm.addEventListener("submit", onSubmitSearch);
    }

    // 테이블 클릭 (이벤트 위임)
    const boardTable = document.getElementById("boardTable");
    if (boardTable) {
      boardTable.addEventListener("click", onTableClick);
    }
  }

  function onSubmitSearch(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const searchVO = {
      searchCondition: formData.get("searchCondition"),
      searchKeyword: formData.get("searchKeyword"),
      pageIndex: 1,
    };

    loadBoardList(searchVO);
  }

  function onTableClick(event) {
    const target = event.target;

    if (target.classList.contains("btn-delete")) {
      const boardId = target.dataset.boardId;
      deleteBoardItem(boardId);
    } else if (target.classList.contains("board-title")) {
      const boardId = target.dataset.boardId;
      location.href = `/board/detail.do?boardId=${boardId}`;
    }
  }

  async function loadBoardList(searchVO = {}) {
    try {
      showLoading(true);

      const response = await callApi({
        url: "/api/v1/board",
        method: "GET",
        data: Object.assign({ pageIndex: currentPage }, searchVO),
      });

      if (response.success) {
        displayBoardList(response.data.resultList);
      }
    } catch (error) {
      alert("게시판 목록을 불러오는데 실패했습니다.");
    } finally {
      showLoading(false);
    }
  }

  function displayBoardList(boardList) {
    const tbody = document.querySelector("#boardTable tbody");
    if (!tbody) return;

    if (!boardList || boardList.length === 0) {
      tbody.innerHTML =
        '<tr><td colspan="5">조회된 데이터가 없습니다.</td></tr>';
      return;
    }

    const rows = boardList.map((board) => createBoardRow(board));
    tbody.innerHTML = "";
    rows.forEach((row) => tbody.appendChild(row));
  }

  function createBoardRow(board) {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${Security.escapeHtml(board.boardId)}</td>
      <td>
        <a href="#" class="board-title" data-board-id="${board.boardId}">
          ${Security.escapeHtml(board.title)}
        </a>
      </td>
      <td>${Security.escapeHtml(board.writer)}</td>
      <td>${formatDate(board.regDate)}</td>
      <td>
        <button type="button" class="btn btn-danger btn-delete" 
                data-board-id="${board.boardId}">삭제</button>
      </td>
    `;

    return row;
  }

  async function deleteBoardItem(boardId) {
    if (!confirm("정말 삭제하시겠습니까?")) return;

    try {
      const response = await callApi({
        url: "/api/v1/board/delete.do",
        method: "POST",
        data: { boardId: boardId },
      });

      if (response.success) {
        alert("삭제되었습니다.");
        loadBoardList();
      }
    } catch (error) {
      alert("삭제 중 오류가 발생했습니다.");
    }
  }

  function showLoading(show) {
    const loadingDiv = document.getElementById("loading");
    if (loadingDiv) {
      loadingDiv.style.display = show ? "block" : "none";
    }
  }

  function formatDate(dateString) {
    if (!dateString) return "";
    const date = new Date(dateString);
    return date.toLocaleDateString("ko-KR");
  }
})();
```

---

## 11. 권장 라이브러리

### 11.1 선택적 사용 라이브러리
- **Chart.js**: 차트 생성용
- **Polyfill**: 브라우저 호환성 지원
- **기타**: 반드시 필요한 경우에만 최소한으로 추가

> [!IMPORTANT] 주의사항
> 이 가이드라인은 권장사항입니다. 프로젝트 특성에 맞게 조정하여 사용하시기 바랍니다.
