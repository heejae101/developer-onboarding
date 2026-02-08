# RAG 임베딩 및 검색 시스템 개발 가이드

이 문서는 현재 프로젝트에 구현된 **RAG(Retrieval-Augmented Generation)** 시스템의 작동 원리와 임베딩 과정을 설명합니다.

## 1. 시스템 아키텍처

현재 RAG 시스템은 별도의 벡터 데이터베이스(ChromaDB, Pinecone 등)를 사용하지 않고, **In-Memory** 방식으로 경량화되어 구현되어 있습니다.

### 주요 모듈 (`agent/src/agent/rag_modules.py`)

1.  **RuleLoader**:
    *   `rules/` 폴더 내의 마크다운(`.md`) 파일들을 읽어옵니다.
    *   헤더(`#`) 단위로 문서를 청크(Chunk)로 분할하여 의미 단위의 텍스트 블록을 생성합니다.

2.  **SimpleVectorStore**:
    *   `numpy`를 사용한 경량 벡터 저장소입니다.
    *   문서의 임베딩 벡터를 메모리에 저장하고, **코사인 유사도(Cosine Similarity)** 계산을 통해 검색을 수행합니다.

3.  **RAGManager**:
    *   전체 프로세스를 조율하는 매니저 클래스입니다.
    *   앱 시작 시 룰을 로딩하고 임베딩을 생성하여 인덱스를 구축합니다.

---

## 2. 임베딩(Embedding) 과정

임베딩은 텍스트를 기계가 이해할 수 있는 고차원 벡터(숫자 배열)로 변환하는 과정입니다.

### 사용 모델
`config.py` 설정에 따라 두 가지 모드를 지원합니다:

1.  **Local Mode (Ollama)**
    *   설정: `LLM_MODE=local`
    *   모델: `nomic-embed-text`
    *   특징: 로컬에서 동작하므로 비용이 들지 않고 보안에 강력합니다. `ollama pull nomic-embed-text` 명령어로 모델을 받아야 합니다.

2.  **API Mode (OpenAI)**
    *   설정: `LLM_MODE=api`
    *   모델: `text-embedding-3-small`
    *   특징: 더 높은 정확도를 제공하지만 비용이 발생합니다.

### 코드 흐름 (`src/llm/client.py`)

```python
# OllamaClient (Local)
def embed(self, text: str) -> list[float]:
    response = self.ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]
```

---

## 3. 검색 로직 (Vector Search)

사용자가 질문을 던졌을 때의 검색 과정입니다:

1.  **Query Embedding**: 사용자의 질문(Query)을 동일한 임베딩 모델을 사용해 벡터로 변환합니다.
2.  **Similarity Calculation**: 저장된 룰 청크들의 벡터와 질문 벡터 간의 유사도를 계산합니다.
    *   공식: `dot(A, B) / (norm(A) * norm(B))`
3.  **Top-K Retrieval**: 유사도가 가장 높은 상위 K개(기본 3개)의 문서를 반환합니다.

## 4. 확장 및 유지보수

*   **새로운 룰 추가**: `rules/` 폴더에 마크다운 파일을 추가하면, 시스템 재시작 시 자동으로 인덱싱됩니다.
*   **성능 개선**: 데이터가 많아질 경우 `FAISS`나 `ChromaDB` 같은 전문 벡터 DB로 교체할 수 있습니다. (`SimpleVectorStore`만 교체하면 됨)
