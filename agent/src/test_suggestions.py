import sys
from pathlib import Path

# Add project root to python path (parent of src)
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agent.tools import GuardrailsTool

def test_suggestions():
    print("Generating suggestions...")
    try:
        suggestion = GuardrailsTool.suggest_alternative("잘못된 질문")
        print("-" * 50)
        print(suggestion)
        print("-" * 50)
    except Exception as e:
        print(f"❌ Failed to get suggestions: {e}")

if __name__ == "__main__":
    test_suggestions()
