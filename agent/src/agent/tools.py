"""
MCP Tools - File operations for the agent
"""
import os
from pathlib import Path
from typing import List, Optional


class FileSearchTool:
    """Search for files in the project"""

    def __init__(self, project_root: str | Path | None = None):
        if project_root is None:
            project_root = Path(__file__).resolve().parents[3]
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
        "퇴근": "퇴근은 칼퇴가 국룰이죠. 개발 질문이 있으시면 말씀해주세요.",
        "힘들": "힘내세요. 개발 관련 도움이 필요하시면 질문해주세요.",
        "피곤": "커피 한잔 어때요. 개발 질문 있으시면 말씀해주세요.",
        "안녕": "안녕하세요. 개발/온보딩 관련 질문이 있으시면 도와드릴게요.",
        "하이": "반가워요. 개발 관련 질문이 있으시면 말씀해주세요.",
        "default": "저는 개발/온보딩 도우미예요. 개발 관련 질문을 해주세요."
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
                return False, "부적절한 표현이 감지되었습니다. 예의 바른 표현으로 다시 질문해주세요."
        
        # 2. 탈옥 시도 체크 - API 안 태움 (빠른 필터)
        for jailbreak in GuardrailsTool.JAILBREAK_PATTERNS:
            if jailbreak in question_lower:
                return False, "해당 요청은 처리할 수 없습니다. 개발/온보딩 관련 질문을 해주세요."
        
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
                return False, f"'{blocked}' 관련 질문은 제 전문 분야가 아니에요.\n\n개발/온보딩 관련 질문을 해주세요."
        
        # 5. 너무 짧은 입력 (1-2글자) - API 안 태움
        if len(question.strip()) < 3:
            return False, "좀 더 구체적으로 질문해주세요."
            
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
                    return False, "[Kanana] 유해한 콘텐츠가 감지되었습니다."
                if not details["legal_safety"]:
                    return False, "[Kanana] 법적 위험(개인정보/저작권)이 감지되었습니다."
                if not details["prompt_safety"]:
                    return False, "[Kanana] 프롬프트 인젝션 공격이 감지되었습니다."
                    
        except Exception as e:
            # 모델 로드 실패 시 로그 남기고 일단 통과 (서비스 중단 방지)
            print(f"Kanana Safeguard Error: {e}")
        
        return True, ""
    
    @staticmethod
    def suggest_alternative(question: str) -> str:
        """Suggest valid question alternatives"""
        try:
            from src.agent.rag_modules import RAGManager
            rag_manager = RAGManager()
            topics = rag_manager.get_suggested_topics(limit=5)
            
            if topics:
                suggestions = "\n".join([f'- "{topic} 알려줘"' for topic in topics])
                return f"""
프로젝트 룰에서 발견된 다음 주제들로 질문해보세요:
{suggestions}
"""
        except Exception as e:
            print(f"Failed to get dynamic suggestions: {e}")
            
        # Fallback to static suggestions
        return """
다음과 같은 질문을 해주세요:
- "Spring Boot에서 API 만드는 규칙 알려줘"
- "UserController 파일 찾아줘"
- "프로젝트 구조 설명해줘"
- "이 코드 리뷰해줘"
"""


class RuleSearchTool:
    """Search project rules using RAG"""
    
    def __init__(self):
        from src.agent.rag_modules import RAGManager
        # Initialize RAG Manager (loads rules and builds index)
        self.rag_manager = RAGManager()
        
    def search(self, query: str) -> str:
        """
        Search for project rules related to the query
        
        Args:
            query: Question about rules/standards (e.g., "naming convention", "api style")
            
        Returns:
            Formatted string with top relevant rules
        """
        results = self.rag_manager.search(query)
        
        if not results:
            return "NO_RULES: 관련 규칙을 찾을 수 없습니다."

        response = f"'{query}' 관련 프로젝트 규칙:\n\n"
        
        for i, result in enumerate(results, 1):
            doc = result["document"]
            score = result["score"]
            response += f"{i}. **{doc['header']}** (유사도: {score:.2f})\n"
            response += f"   - 출처: `{doc['source']}`\n"
            # Show snippet (first 3 lines or limited chars) to avoid overwhelming
            content_snippet = '\n'.join(doc['content'].split('\n')[:5])
            response += f"   - 내용:\n```markdown\n{content_snippet}\n...\n```\n\n"
            
        return response

class FileManagementTool:
    """Tool for creating, editing, and managing files"""

    def __init__(self, project_root: str | Path | None = None):
        if project_root is None:
            project_root = Path(__file__).resolve().parents[3]
        self.project_root = Path(project_root)
        
    def create_file(self, path: str, content: str) -> str:
        """Create a new file with content"""
        try:
            full_path = self._resolve_path(path)
            
            # Create directories if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return f"File created successfully: {path}"
        except Exception as e:
            return f"Failed to create file: {e}"
            
    def edit_file(self, path: str, edit_instruction: str, content: str) -> str:
        """Edit an existing file (Overwrite for now)"""
        try:
            full_path = self._resolve_path(path)
            
            if not full_path.exists():
                return f"File not found: {path}"
                
            # For now, we support full overwrite or append.
            # Complex editing (diff) might need LLM assistance,
            # but here we assume 'content' is the new content.
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return f"File updated successfully: {path}"
        except Exception as e:
            return f"Failed to edit file: {e}"
            
    def delete_file(self, path: str) -> str:
        """Delete a file"""
        try:
            full_path = self._resolve_path(path)
            
            if not full_path.exists():
                return f"File not found: {path}"
                
            os.remove(full_path)
            return f"File deleted successfully: {path}"
        except Exception as e:
            return f"Failed to delete file: {e}"
            
    def _resolve_path(self, path: str) -> Path:
        """Resolve path against project root"""
        if path.startswith("/"):
            # Check if it starts with project root
            if path.startswith(str(self.project_root)):
                return Path(path)
            # If absolute but not in project, force it (or restrict it?)
            # For safety, let's join with project root if it looks relative-ish or just trust user provided abs path if safe.
            # But safer to treat all as relative to root unless explicitly allowed.
            # Simple approach: If absolute, use it. If relative, join with root.
            return Path(path)
        return self.project_root / path


class CommandExecutor:
    """Execute shell commands safely"""

    ALLOWED_COMMANDS = ["ls", "cat", "grep", "find", "pwd", "mkdir", "rm", "cp", "mv", "npm", "node", "java", "javac", "python", "echo", "touch"]

    def __init__(self, project_root: str | Path | None = None):
        if project_root is None:
            project_root = Path(__file__).resolve().parents[3]
        self.project_root = Path(project_root)

    def run_command(self, command: str) -> str:
        """Run a shell command"""
        import subprocess
        import shlex
        
        # Security check
        cmd_parts = shlex.split(command)
        if not cmd_parts:
            return "Empty command"
            
        base_cmd = cmd_parts[0]
        if base_cmd not in self.ALLOWED_COMMANDS and not base_cmd.endswith(".sh"): # Allow scripts
             return f"Command not allowed: {base_cmd}"
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=str(self.project_root),
                timeout=30
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\n[Stderr]\n{result.stderr}"
                
            return output if output.strip() else "Command executed (no output)"
            
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Execution failed: {e}"
