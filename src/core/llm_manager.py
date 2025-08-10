from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from src.config.settings import get_api_key

def get_available_providers(config):
    available = {}
    
    for provider_name, provider_config in config["llm_providers"].items():
        if not provider_config.get("enabled", False):
            continue
            
        api_key = get_api_key(provider_name)
        
        if provider_name == "azure_openai":
            from src.config.settings import get_azure_endpoint
            endpoint = get_azure_endpoint()
            if api_key and endpoint:
                available[provider_name] = {
                    "models": provider_config["models"],
                    "default_model": provider_config["default_model"],
                    "temperature": provider_config["temperature"]
                }
        elif api_key:
            available[provider_name] = {
                "models": provider_config["models"],
                "default_model": provider_config["default_model"],
                "temperature": provider_config["temperature"]
            }
    
    return available

def create_llm(provider_name, model_name, config):
    provider_config = config["llm_providers"][provider_name]
    api_key = get_api_key(provider_name)
    
    if not api_key:
        raise ValueError(f"API key not found for {provider_name}")
    
    temperature = provider_config["temperature"]
    
    if provider_name == "openai":
        return ChatOpenAI(model=model_name, temperature=temperature, api_key=api_key)
    elif provider_name == "azure_openai":
        from src.config.settings import get_azure_endpoint
        endpoint = get_azure_endpoint()
        api_version = provider_config.get("api_version", "2024-02-15-preview")
        return AzureChatOpenAI(
            azure_deployment=model_name,
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
            temperature=temperature
        )
    elif provider_name == "anthropic":
        return ChatAnthropic(model=model_name, temperature=temperature, api_key=api_key)
    elif provider_name == "google":
        return ChatGoogleGenerativeAI(model=model_name, temperature=temperature, api_key=api_key)
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")

def create_conversation_chain(provider_name, model_name, config, memory_window=3):
    llm = create_llm(provider_name, model_name, config)
    memory = ConversationBufferWindowMemory(k=memory_window, return_messages=True)
    
    conversation = ConversationChain(llm=llm, memory=memory, verbose=False)
    return conversation

def add_summary_to_memory(conversation_chain, summary, url):
    context = f"I summarized the webpage at {url}. Here's the summary: {summary}"
    conversation_chain.predict(input=context)
