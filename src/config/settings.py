import yaml
import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    with open("conf/config.yaml", "r") as file:
        return yaml.safe_load(file)

def load_prompts():
    with open("prompts/prompts.yaml", "r") as file:
        return yaml.safe_load(file)

def get_api_key(provider_name):
    config = load_config()
    provider_config = config["llm_providers"][provider_name]
    return os.getenv(provider_config["api_key_env"])

def get_azure_endpoint():
    return os.getenv("AZURE_OPENAI_ENDPOINT")
