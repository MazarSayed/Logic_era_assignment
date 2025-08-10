import os
import sys

def ensure_project_root():
    if not os.path.exists("conf/config.yaml"):
        print("❌ Error: conf/config.yaml not found")
        print("Please run this script from the project root directory")
        sys.exit(1)

def create_env_template():
    env_file = ".env"
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write("""# Webpage Summarizer API Keys
# Add your API keys here (at least one is required)

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Azure OpenAI (optional)
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here

# Anthropic API Key (optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google API Key (optional)
GOOGLE_API_KEY=your_google_api_key_here
""")
        print(f"✅ Created {env_file} template")
        print("Please add your API keys to the .env file")

def check_dependencies():
    try:
        import streamlit
        import fastapi
        import langchain
        import requests
        import yaml
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: uv sync")
        return False
