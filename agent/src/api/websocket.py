"""
WebSocket endpoints for AI Agent
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.agent import get_agent_graph, AgentState
import uuid
import json
import asyncio

router = APIRouter()

@router.websocket("/ws/ai-stream")
async def websocket_ai_stream(websocket: WebSocket):
    """
    WebSocket endpoint for streaming AI responses.
    Connected by Spring Boot backend.
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive message from Spring Boot
            data = await websocket.receive_text()
            request = json.loads(data)
            
            message = request.get("message", "")
            thread_id = request.get("thread_id", str(uuid.uuid4()))
            user_id = request.get("user_id", 0)
            
            # Initial state
            state: AgentState = {
                "thread_id": thread_id,
                "user_id": user_id,
                "message": message,
                "stream_tokens": []
            }
            
            # Run LangGraph with streaming
            graph = get_agent_graph()
            
            # Streaming response
            async for event in graph.astream(state):
                # Send updates to client
                for key, value in event.items():
                    print(f"DEBUG: Graph Node '{key}' finished")
                    
                    if key == "complete":
                        # Final response from the complete node
                        await websocket.send_text(json.dumps({
                            "type": "complete",
                            "content": value.get("final_response", ""),
                            "intent": value.get("next_node")
                        }))
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "content": str(e)
            }))
        except:
            pass
