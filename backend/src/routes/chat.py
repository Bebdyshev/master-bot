from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from src.schemas.chat import ChatRequest
from src.agents.support_agent import StudentSupportAgent
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/chat")
async def chat(request: ChatRequest):
    """
    AI chat endpoint for student support
    Automatically detects problems and provides solutions using LangChain + Groq
    """
    try:
        # Ensure student_id is a string
        student_id = str(request.student_id) if request.student_id else "unknown"
        
        # Create agent for this student
        agent = StudentSupportAgent(student_id=student_id)
        
        # Convert history to dict format
        history = [{"role": msg.role, "content": msg.content} for msg in request.history]
        
        # Get response from agent (now returns dict with response and ticket)
        result = agent.chat(request.message, chat_history=history)
        
        # Build response
        response_data = {
            "response": result.get("response", ""),
            "student_id": student_id
        }
        
        # Add ticket data if present
        if result.get("ticket"):
            response_data["ticket"] = result["ticket"]
        
        return response_data
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming version of chat endpoint
    Returns responses in real-time as they're generated
    """
    try:
        # Ensure student_id is a string
        student_id = str(request.student_id) if request.student_id else "unknown"
        
        agent = StudentSupportAgent(student_id=student_id)
        history = [{"role": msg.role, "content": msg.content} for msg in request.history]
        
        async def generate():
            async for chunk in agent.chat_stream(request.message, chat_history=history):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    except Exception as e:
        logger.error(f"Chat stream error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
