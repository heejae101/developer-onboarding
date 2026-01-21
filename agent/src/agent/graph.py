"""
LangGraph graph builder
"""
from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent.nodes import (
    router_node,
    search_rules_node,
    verify_rules_node,
    code_review_node,
    think_node,
    act_node,
    should_continue,
    complete_node,
)


def build_agent_graph() -> StateGraph:
    """Build and compile the agent graph"""
    
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("router", router_node)
    graph.add_node("search", search_rules_node)
    graph.add_node("verify", verify_rules_node)
    graph.add_node("code_review", code_review_node)
    graph.add_node("think", think_node)
    graph.add_node("act", act_node)
    graph.add_node("complete", complete_node)
    
    # Set entry point
    graph.set_entry_point("router")
    
    # Router conditional edges
    graph.add_conditional_edges(
        "router",
        lambda state: state.get("next_node", "search"),
        {
            "search": "search",
            "verify": "verify",
            "code_review": "code_review",
            "autonomous": "think",
        }
    )
    
    # Simple paths to complete
    graph.add_edge("search", "complete")
    graph.add_edge("verify", "complete")
    graph.add_edge("code_review", "complete")
    
    # Autonomous loop
    graph.add_edge("think", "act")
    graph.add_conditional_edges(
        "act",
        should_continue,
        {
            "continue": "think",
            "complete": "complete",
        }
    )
    
    # End
    graph.add_edge("complete", END)
    
    return graph.compile()


# Singleton graph instance
_graph = None


def get_agent_graph():
    """Get or create the agent graph"""
    global _graph
    if _graph is None:
        _graph = build_agent_graph()
    return _graph
