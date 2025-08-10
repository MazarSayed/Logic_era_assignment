"""
Script to run the Webpage Summarizer API
"""

import uvicorn
from src.utils.utils import ensure_project_root, create_env_template, check_dependencies

def main():
    print("🚀 Starting Webpage Summarizer API...")
    
    # Check if we're in the right directory
    ensure_project_root()
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Create .env template if needed
    create_env_template()
    
    # Run the FastAPI server
    print("🌐 Starting API server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    exit(main())
