# 📄 Webpage Summarizer

A high-performance web application that intelligently summarizes webpages using multiple AI providers. Built with FastAPI backend and Streamlit frontend for optimal speed and user experience.

## ✨ Key Features

- **⚡ Ultra-Fast Processing**: Optimized scraping and chunking (25x performance improvement)
- **🤖 Multi-Provider AI**: OpenAI, Anthropic, Google, and Azure OpenAI models with automatic selection
- **🎯 Smart Content Extraction**: Intelligent main content detection and text processing
- **📱 Modern Web Interface**: Responsive Streamlit frontend with real-time feedback
- **🔗 RESTful API**: Complete API access for programmatic integration
- **🛡️ Robust Error Handling**: Graceful degradation and comprehensive error management
- **📊 Mock Mode**: Works without API keys for testing and demonstration
- **💬 Conversation Memory**: Follow-up questions with context awareness

## 🚀 Detailed Setup Instructions

### Prerequisites

Before starting, ensure you have:
- **Python 3.9 or higher** installed on your system
- **Git** for cloning the repository
- **Internet connection** for downloading packages and API access

### Step 1: Clone the Repository

```bash
# Clone the repository to your local machine
git clone <your-repository-url>
cd Logic_era_assignment

# Verify you're in the correct directory
ls -la
# You should see files like: app.py, run_api.py, models.py, etc.
```

### Step 2: Install Python Package Manager (uv)

This project uses `uv` for fast Python package management. Install it first:

#### On macOS/Linux:
```bash
# Install uv using curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart your terminal or reload shell configuration
source ~/.bashrc  # or source ~/.zshrc for zsh users

# Verify installation
uv --version
```

#### On Windows:
```bash
# Install using pip
pip install uv

# Verify installation
uv --version
```

#### Alternative: Using pip (if uv is not available)
```bash
# Install virtual environment tools
pip install virtualenv

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Project Dependencies

#### Using uv (Recommended):
```bash
# Install all dependencies from pyproject.toml
uv sync

# Verify installation
uv run python -c "import fastapi, streamlit, langchain; print('All packages installed successfully!')"
```

#### Using pip (Alternative):
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt

# Or install packages individually
pip install fastapi uvicorn streamlit langchain langchain-openai langchain-anthropic langchain-google-genai beautifulsoup4 requests pydantic pyyaml python-dotenv
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
# Create .env file
touch .env

# Edit the file with your preferred text editor
# On macOS/Linux:
nano .env
# On Windows:
notepad .env
```

Add your API keys to the `.env` file:

```bash
# Required: At least one API key is needed
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Additional providers for more AI model options
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here

# Note: Replace 'your_*_key_here' with your actual API keys
# You can get these from:
# - OpenAI: https://platform.openai.com/api-keys
# - Anthropic: https://console.anthropic.com/
# - Google: https://makersuite.google.com/app/apikey
# - Azure OpenAI: Your Azure portal
```

### Step 5: Verify Configuration

Check that your configuration files are properly set up:

```bash
# Verify config files exist
ls -la conf/
ls -la prompts/

# Check config.yaml content
cat conf/config.yaml

# Check prompts.yaml content
cat prompts/prompts.yaml
```

## 🏃‍♂️ Running the Application

### Option 1: Run Both Services (Recommended for Development)

#### Terminal 1: Start the FastAPI Backend
```bash
# Make sure you're in the project root directory
cd Logic_era_assignment

# Start the API server
uv run python run_api.py

# You should see output like:
# 🚀 Starting Webpage Summarizer API...
# 🌐 Starting API server...
# 📖 API Documentation: http://localhost:8000/docs
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

#### Terminal 2: Start the Streamlit Frontend
```bash
# Open a new terminal window/tab
cd Logic_era_assignment

# Start the Streamlit application
uv run streamlit run app.py

# You should see output like:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://192.168.x.x:8501
```

### Option 2: Run Services Individually

#### Start Only the API Server:
```bash
uv run python run_api.py
```
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Base URL**: http://localhost:8000

#### Start Only the Streamlit App:
```bash
uv run streamlit run app.py
```
- **Web Interface**: http://localhost:8501
- **Note**: The app will show an error if the API server is not running

### Option 3: Using pip (if uv is not available)

```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Terminal 1: Start API
python run_api.py

# Terminal 2: Start Streamlit
streamlit run app.py
```

## 🌐 Accessing the Application

### Web Interface (Streamlit)
- **URL**: http://localhost:8501
- **Features**: 
  - URL input for webpage summarization
  - Provider selection dropdown
  - Real-time processing feedback
  - Chat interface for follow-up questions
  - Error handling and status messages

### API Endpoints (FastAPI)
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Available Providers**: http://localhost:8000/providers
- **Summarize Endpoint**: POST http://localhost:8000/summarize
- **Chat Endpoint**: POST http://localhost:8000/chat

## 🧪 Testing the Setup

### 1. Test API Health
```bash
# Check if API is running
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "service": "Webpage Summarizer API"}
```

### 2. Test Summarization
```bash
# Test the summarize endpoint
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Expected response:
# {"summary": "...", "main_topic": "...", "session_id": "..."}
```

### 3. Test Web Interface
1. Open http://localhost:8501 in your browser
2. Enter a test URL (e.g., https://example.com)
3. Click "🚀 Summarize"
4. Verify you get a summary response

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "uv: command not found"
**Solution**: Install uv properly or use pip alternative
```bash
# Alternative using pip
pip install virtualenv
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

#### Issue 2: "Port 8000 is already in use"
**Solution**: Kill the process using the port
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

#### Issue 3: "Port 8501 is already in use"
**Solution**: Streamlit will automatically use the next available port
```bash
# Or manually specify a different port
uv run streamlit run app.py --server.port 8502
```

#### Issue 4: "No module named 'langchain'"
**Solution**: Dependencies not installed properly
```bash
# Reinstall dependencies
uv sync --reinstall

# Or with pip
pip install -r requirements.txt
```

#### Issue 5: "API server is not running"
**Solution**: Start the API server first
```bash
# Terminal 1: Start API
uv run python run_api.py

# Terminal 2: Start Streamlit
uv run streamlit run app.py
```

#### Issue 6: "Invalid API key" or "No API keys configured"
**Solution**: Check your .env file
```bash
# Verify .env file exists and has content
cat .env

# Make sure API keys are properly formatted
# Correct: OPENAI_API_KEY=sk-1234567890abcdef
# Wrong: OPENAI_API_KEY=your_openai_key_here
```

### Performance Issues

#### Slow Response Times
- Check your internet connection
- Verify API key validity
- Try a different AI provider
- Check if the target webpage is accessible

#### Memory Issues
- Restart the application
- Check system resources
- Reduce content size limits in `conf/config.yaml`

## 📁 Project Structure

```
Logic_era_assignment/
├── src/
│   ├── api/                    # API server and client
│   │   ├── server.py          # FastAPI server implementation
│   │   └── client.py          # API client functions
│   ├── config/                # Configuration management
│   │   └── settings.py        # Environment and config loading
│   ├── core/                  # Core functionality
│   │   ├── web_scraper.py     # Web content extraction
│   │   ├── text_processor.py  # Text processing and summarization
│   │   └── llm_manager.py     # AI model management
│   ├── utils/                 # Utility functions
│   │   └── utils.py           # Helper functions
│   └── web/                   # Web interface
│       └── streamlit_app.py   # Streamlit application
├── conf/
│   └── config.yaml            # Application configuration
├── prompts/
│   └── prompts.yaml           # AI prompt templates
├── app.py                     # Streamlit entry point
├── run_api.py                 # API server entry point
├── models.py                  # Pydantic data models
├── pyproject.toml             # Project dependencies
├── .env                       # Environment variables (create this)
└── README.md                  # This file
```

## 🌟 Performance Highlights

- **⚡ 25x Faster**: Reduced processing time from 112s to 4.4s
- **🎯 Smart Scraping**: Intelligent content extraction with size limits
- **🔧 Optimized Chunking**: Efficient text processing for faster LLM responses
- **📱 Responsive UI**: Real-time feedback and error handling
- **🤖 Auto-Selection**: Automatic provider and model selection
- **💬 Memory Management**: Conversation context for follow-up questions

## 📖 API Documentation

Once the API is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### API Usage Examples

```bash
# Summarize a webpage
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Chat with summary (requires session_id from summarize)
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id", "question": "What are the main points?"}'

# Get available providers
curl http://localhost:8000/providers
```

## 🛠️ Requirements

- **Python**: 3.9 or higher
- **Package Manager**: uv (recommended) or pip
- **API Keys**: At least one AI provider API key
- **Internet**: Connection required for web scraping and AI API calls
- **System**: 4GB RAM minimum, 8GB recommended

## 📚 Additional Documentation

- **[Implementation.md](Implementation.md)**: Detailed technical implementation guide
- **Interactive API Docs**: http://localhost:8000/docs (when server is running)
- **Streamlit Documentation**: https://docs.streamlit.io/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/

## 🏗️ Architecture

```
┌─────────────────┐    HTTP Requests    ┌─────────────────┐
│   Streamlit     │ ─────────────────→  │   FastAPI       │
│   Frontend      │                     │   Backend       │
│   (Port 8501)   │ ←───────────────── │   (Port 8000)   │
└─────────────────┘    JSON Responses   └─────────────────┘
        │                                        │
        │                                        │
        v                                        v
┌─────────────────┐                     ┌─────────────────┐
│   API Client    │                     │   LangChain     │
│   Functions     │                     │   Agent Core    │
└─────────────────┘                     └─────────────────┘
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use and modify!

## 🆘 Need Help?

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure API keys are properly configured
4. Check that both services are running
5. Review the error messages for specific guidance
