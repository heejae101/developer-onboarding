import sys
from pathlib import Path

# Add project root to python path (parent of src)
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agent.tools import RuleSearchTool

def test_rag():
    print("Initializing RuleSearchTool...")
    try:
        tool = RuleSearchTool()
        print("Initialization successful")
    except Exception as e:
        print(f"Initialization failed: {e}")
        return

    queries = [
        "변수 명명 규칙이 뭐야?",
        "API 스타일 가이드 알려줘",
        "스타일링은 어떻게 해?"
    ]
    
    print("\nStarting search tests...")
    for query in queries:
        print(f"\nTarget Query: {query}")
        try:
            result = tool.search(query)
            print("-" * 50)
            print(result)
            print("-" * 50)
        except Exception as e:
            print(f"Search failed: {e}")

if __name__ == "__main__":
    test_rag()
