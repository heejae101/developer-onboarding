"""
MCP Tools - File operations for the agent
"""
import os
from pathlib import Path
from typing import List, Optional


class FileSearchTool:
    """Search for files in the project"""
    
    def __init__(self, project_root: str = "/Users/chaehuijae/Desktop/가이드"):
        self.project_root = Path(project_root)
    
    def search_files(self, query: str, extensions: Optional[List[str]] = None) -> List[dict]:
        """
        Search for files matching the query
        
        Args:
            query: Search term (filename or content)
            extensions: File extensions to filter (e.g., ['.java', '.md'])
        
        Returns:
            List of matching files with metadata
        """
        results = []
        
        if extensions is None:
            extensions = ['.java', '.md', '.py', '.js', '.jsx', '.ts', '.tsx']
        
        for ext in extensions:
            for file_path in self.project_root.rglob(f"*{ext}"):
                # Skip hidden files and directories
                if any(part.startswith('.') for part in file_path.parts):
                    continue
                
                # Check if filename matches
                if query.lower() in file_path.name.lower():
                    results.append({
                        "path": str(file_path),
                        "name": file_path.name,
                        "type": ext,
                        "match_type": "filename"
                    })
        
        return results[:10]  # Limit to 10 results
    
    def read_file(self, file_path: str, max_lines: int = 100) -> dict:
        """
        Read file contents
        
        Args:
            file_path: Absolute path to file
            max_lines: Maximum number of lines to read
        
        Returns:
            File content and metadata
        """
        try:
            path = Path(file_path)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                content = ''.join(lines[:max_lines])
                
            return {
                "path": str(path),
                "name": path.name,
                "content": content,
                "total_lines": len(lines),
                "truncated": len(lines) > max_lines
            }
        except Exception as e:
            return {
                "error": str(e),
                "path": file_path
            }


class GuardrailsTool:
    """Validate if questions are within project scope and filter harmful content"""
    
    ALLOWED_TOPICS = [
        "spring boot", "java", "api", "controller", "service", "repository",
        "react", "frontend", "컴포넌트", "component",
        "온보딩", "onboarding", "규칙", "rule", "코드", "code",
        "python", "fastapi", "langgraph", "에이전트", "agent",
        "프로젝트", "project", "개발", "develop", "파일", "file"
    ]
    
    # 범위 밖 주제
    BLOCKED_TOPICS = [
        "날씨", "weather", "뉴스", "news", "요리", "recipe",
        "영화", "movie", "음악", "music", "게임", "game",
        "주식", "stock", "비트코인", "bitcoin", "로또", "lotto"
    ]
    
    # 욕설 필터 (한국어 + 영어)
    PROFANITY_PATTERNS = [
        "시발", "씨발", "ㅅㅂ", "ㅆㅂ", "sibal", "fuck", "shit", "damn",
        "개새끼", "ㄱㅅㄲ", "병신", "ㅂㅅ", "지랄", "ㅈㄹ",
        "미친", "ㅁㅊ", "꺼져", "닥쳐", "asshole", "bastard"
    ]
    
    # 탈옥 시도 패턴
    JAILBREAK_PATTERNS = [
        "ignore previous", "이전 지시 무시", "forget your instructions",
        "지시를 무시", "you are now", "너는 이제", "pretend to be",
        "~인 척", "역할극", "roleplay", "dan mode", "developer mode",
        "개발자 모드", "제한 해제", "remove restrictions",
        "system prompt", "시스템 프롬프트", "reveal your prompt"
    ]
    
    # 잡담/감정표현 (LLM 안 태우고 빠르게 응답)
    CASUAL_PATTERNS = [
        "퇴근", "힘들", "피곤", "졸려", "배고파", "심심",
        "안녕", "하이", "hi", "hello", "ㅋㅋ", "ㅎㅎ", "ㄱㄱ",
        "ㅇㅇ", "ㄴㄴ", "뭐해", "뭐함"
    ]
    
    CASUAL_RESPONSES = {
        "퇴근": "퇴근은 칼퇴가 국룰이죠! 🏃 개발 질문이 있으시면 말씀해주세요.",
        "힘들": "힘내세요! 💪 개발 관련 도움이 필요하시면 질문해주세요.",
        "피곤": "커피 한잔 어때요? ☕ 개발 질문 있으시면 말씀해주세요.",
        "안녕": "안녕하세요! 👋 개발/온보딩 관련 질문이 있으시면 도와드릴게요.",
        "하이": "반가워요! 개발 관련 질문이 있으시면 말씀해주세요.",
        "default": "저는 개발/온보딩 도우미예요. 개발 관련 질문을 해주세요! 🤖"
    }
    
    @staticmethod
    async def is_valid_question(question: str) -> tuple[bool, str]:
        """
        Check if question is valid and within scope
        
        Returns:
            (should_call_llm, response_if_blocked)
        """
        question_lower = question.lower()
        
        # 1. 욕설 체크 - API 안 태움 (빠른 필터)
        for profanity in GuardrailsTool.PROFANITY_PATTERNS:
            if profanity in question_lower:
                return False, "⚠️ 부적절한 표현이 감지되었습니다. 예의 바른 표현으로 다시 질문해주세요."
        
        # 2. 탈옥 시도 체크 - API 안 태움 (빠른 필터)
        for jailbreak in GuardrailsTool.JAILBREAK_PATTERNS:
            if jailbreak in question_lower:
                return False, "🚫 해당 요청은 처리할 수 없습니다. 개발/온보딩 관련 질문을 해주세요."
        
        # 3. 잡담/감정표현 체크 - API 안 태우고 빠른 응답
        for casual in GuardrailsTool.CASUAL_PATTERNS:
            if casual in question_lower:
                response = GuardrailsTool.CASUAL_RESPONSES.get(
                    casual, 
                    GuardrailsTool.CASUAL_RESPONSES["default"]
                )
                return False, response
        
        # 4. 범위 밖 주제 체크 - API 안 태움
        for blocked in GuardrailsTool.BLOCKED_TOPICS:
            if blocked in question_lower:
                return False, f"📌 '{blocked}' 관련 질문은 제 전문 분야가 아니에요.\n\n개발/온보딩 관련 질문을 해주세요!"
        
        # 5. 너무 짧은 입력 (1-2글자) - API 안 태움
        if len(question.strip()) < 3:
            return False, "❓ 좀 더 구체적으로 질문해주세요!"
            
        # ---------------------------------------------------------
        # 6. Kakao Kanana Safeguard 모델 검증 (정밀 검사)
        # ---------------------------------------------------------
        try:
            from src.agent.kanana_safeguard import get_kanana_safeguard
            import asyncio
            
            # 모델 로딩/추론은 블로킹 작업이므로 별도 스레드에서 실행
            safeguard = get_kanana_safeguard()
            
            # check_all 메서드를 비동기로 실행
            is_safe, details = await asyncio.to_thread(
                safeguard.check_all, question
            )
            
            if not is_safe:
                # 안전하지 않은 경우 사유 분석
                if not details["content_safety"]:
                    return False, "⚠️ [Kanana] 유해한 콘텐츠가 감지되었습니다."
                if not details["legal_safety"]:
                    return False, "⚖️ [Kanana] 법적 위험(개인정보/저작권)이 감지되었습니다."
                if not details["prompt_safety"]:
                    return False, "🚫 [Kanana] 프롬프트 인젝션 공격이 감지되었습니다."
                    
        except Exception as e:
            # 모델 로드 실패 시 로그 남기고 일단 통과 (서비스 중단 방지)
            print(f"⚠️ Kanana Safeguard Error: {e}")
        
        return True, ""
    
    @staticmethod
    def suggest_alternative(question: str) -> str:
        """Suggest valid question alternatives"""
        return """
💡 다음과 같은 질문을 해주세요:
- "Spring Boot에서 API 만드는 규칙 알려줘"
- "UserController 파일 찾아줘"
- "프로젝트 구조 설명해줘"
- "이 코드 리뷰해줘"
"""
