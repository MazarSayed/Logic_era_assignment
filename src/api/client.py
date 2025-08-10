import requests

def check_api_health():
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_api_providers():
    try:
        response = requests.get("http://localhost:8000/providers", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API call failed: {str(e)}"}

def call_api_summarize(url, provider=None, model=None):
    try:
        payload = {"url": url}
        if provider:
            payload["provider"] = provider
        if model:
            payload["model"] = model
        response = requests.post("http://localhost:8000/summarize", json=payload, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API call failed: {str(e)}"}

def call_api_chat(session_id, question):
    try:
        payload = {"session_id": session_id, "question": question}
        response = requests.post("http://localhost:8000/chat", json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Chat API call failed: {str(e)}"}

def call_api_conversation(question, session_id):
    try:
        payload = {"question": question, "session_id": session_id}
        response = requests.post("http://localhost:8000/conversation", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API call failed: {str(e)}"}
