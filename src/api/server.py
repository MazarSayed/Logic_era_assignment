from fastapi import FastAPI, HTTPException
import uvicorn
import uuid
from models import (
    SummarizeRequest,
    SummarizeResponse,
    ChatRequest,
    ChatResponse,
    ConversationRequest,
    ConversationResponse,
    ProvidersResponse,
    HealthResponse
)
from src.config.settings import load_config
from src.core.web_scraper import validate_url, fetch_and_clean_content
from src.core.text_processor import summarize_content
from src.core.llm_manager import (
    get_available_providers,
    create_llm,
    create_conversation_chain,
    add_summary_to_memory
)

app = FastAPI(
    title="Webpage Summarizer API",
    description="API for summarizing webpages using multiple LLM providers",
    version="1.0.0"
)

conversation_sessions = {}

@app.get("/")
async def root():
    return {
        "message": "Webpage Summarizer API",
        "version": "1.0.0",
        "endpoints": {
            "/summarize": "POST - Summarize a webpage",
            "/providers": "GET - List available providers",
            "/conversation": "POST - Ask follow-up questions"
        }
    }

@app.get("/providers", response_model=ProvidersResponse)
async def get_providers():
    config = load_config()
    available_providers = get_available_providers(config)
    
    providers_info = {}
    for provider_name, provider_config in available_providers.items():
        providers_info[provider_name] = {
            "models": provider_config["models"],
            "default_model": provider_config["default_model"]
        }
    
    return ProvidersResponse(
        available_providers=providers_info,
        total_providers=len(providers_info)
    )

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_page(request: SummarizeRequest):
    config = load_config()
    
    from src.config.settings import get_api_key, get_azure_endpoint
    valid_keys = []
    for provider in ["openai", "azure_openai", "anthropic", "google"]:
        key = get_api_key(provider)
        if provider == "azure_openai":
            endpoint = get_azure_endpoint()
            if (key and not key.startswith("your_") and key != "your_api_key_here" and len(key) > 10 and
                endpoint and not endpoint.startswith("your_") and endpoint != "your_azure_endpoint_here"):
                valid_keys.append(provider)
        elif key and not key.startswith("your_") and key != "your_api_key_here" and len(key) > 10:
            valid_keys.append(provider)

    
    available_providers = get_available_providers(config)
    
    requested_provider = getattr(request, 'provider', None)
    requested_model = getattr(request, 'model', None)
    
    if requested_provider and requested_provider in available_providers:
        provider_name = requested_provider
        provider_config = available_providers[provider_name]
        if requested_model and requested_model in provider_config["models"]:
            selected_model = requested_model
        else:
            selected_model = provider_config["default_model"]
    else:
        provider_name = list(available_providers.keys())[0]
        provider_config = available_providers[provider_name]
        selected_model = provider_config["default_model"]
    
    url_str = str(request.url)
    
    is_valid, message = validate_url(url_str, config)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    content, error = fetch_and_clean_content(url_str, config)
    if error:
        raise HTTPException(status_code=422, detail=error)
    
    llm = create_llm(provider_name, selected_model, config)
    summary, main_topic = summarize_content(content, llm)
    
    if summary.startswith("Error"):
        raise HTTPException(status_code=500, detail=summary)
    
    conversation_chain = create_conversation_chain(provider_name, selected_model, config)
    add_summary_to_memory(conversation_chain, summary, url_str)
    
    session_id = str(uuid.uuid4())
    conversation_sessions[session_id] = {
        'conversation_chain': conversation_chain,
        'summary': summary,
        'topic': main_topic,
        'url': url_str
    }
    
    return SummarizeResponse(
        summary=summary,
        main_topic=main_topic,
        session_id=session_id
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_summary(request: ChatRequest):
    if request.session_id not in conversation_sessions:
        raise HTTPException(status_code=404, detail="Chat session not found. Please summarize a webpage first.")
    
    session_data = conversation_sessions[request.session_id]
    conversation_chain = session_data['conversation_chain']
    
    try:
        answer = conversation_chain.predict(input=request.question)
        return ChatResponse(answer=answer, session_id=request.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/conversation", response_model=ConversationResponse)
async def ask_question(request: ConversationRequest):
    if request.session_id not in conversation_sessions:
        raise HTTPException(status_code=404, detail="Conversation session not found")
    
    session_data = conversation_sessions[request.session_id]
    conversation_chain = session_data['conversation_chain']
    answer = conversation_chain.predict(input=request.question)
    
    return ConversationResponse(answer=answer, session_id=request.session_id)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", service="webpage-summarizer-api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
