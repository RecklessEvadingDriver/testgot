"""
WromGPT - A GPT model service with instruction injection
This service provides API endpoints for interacting with a Hugging Face GPT model
with custom instructions injected into the conversation.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import Optional
from contextlib import asynccontextmanager
import threading
import os

# System instructions that will be injected into every conversation
SYSTEM_INSTRUCTIONS = """You are WromGPT, a helpful and knowledgeable AI assistant.
You provide accurate, concise, and helpful responses to user queries.
Always maintain a professional and friendly tone."""

# Thread lock for safe instruction updates
instructions_lock = threading.Lock()

# Model configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gpt2")  # Default to GPT-2, can be changed
tokenizer = None
model = None


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    max_length: Optional[int] = 200
    temperature: Optional[float] = 0.7
    custom_instructions: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    model_used: str


class InstructionsRequest(BaseModel):
    """Request model for updating system instructions"""
    instructions: str


def load_model():
    """Load the Hugging Face model and tokenizer"""
    global tokenizer, model
    
    try:
        print(f"Loading model: {MODEL_NAME}")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        
        # Set pad token if not set
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup: Load model
    load_model()
    yield
    # Shutdown: cleanup if needed
    pass


app = FastAPI(
    title="WromGPT API",
    description="GPT model with instruction injection capabilities",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "WromGPT API",
        "version": "1.0.0",
        "status": "running",
        "model": MODEL_NAME,
        "endpoints": {
            "chat": "/api/chat",
            "instructions": "/api/instructions",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_loaded = model is not None and tokenizer is not None
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded,
        "model_name": MODEL_NAME
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint with instruction injection
    
    Args:
        request: ChatRequest containing the user message and optional parameters
        
    Returns:
        ChatResponse with the model's response
    """
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Use custom instructions if provided, otherwise use system instructions
        with instructions_lock:
            instructions = request.custom_instructions if request.custom_instructions else SYSTEM_INSTRUCTIONS
        
        # Construct the prompt with injected instructions
        prompt = f"{instructions}\n\nUser: {request.message}\n\nAssistant:"
        
        # Tokenize the input
        inputs = tokenizer(prompt, return_tensors="pt", padding=True)
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_length=request.max_length,
                temperature=request.temperature,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
                top_p=0.9,
                num_return_sequences=1
            )
        
        # Decode the response
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the assistant's response (remove the prompt)
        if "Assistant:" in response_text:
            response_text = response_text.split("Assistant:")[-1].strip()
        
        return ChatResponse(
            response=response_text,
            model_used=MODEL_NAME
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@app.get("/api/instructions")
async def get_instructions():
    """Get current system instructions"""
    with instructions_lock:
        return {"instructions": SYSTEM_INSTRUCTIONS}


@app.post("/api/instructions")
async def update_instructions(request: InstructionsRequest):
    """
    Update system instructions that are injected into conversations
    
    Args:
        request: InstructionsRequest containing new instructions
        
    Returns:
        Confirmation message
    """
    global SYSTEM_INSTRUCTIONS
    with instructions_lock:
        SYSTEM_INSTRUCTIONS = request.instructions
        return {
            "status": "success",
            "message": "System instructions updated",
            "instructions": SYSTEM_INSTRUCTIONS
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
