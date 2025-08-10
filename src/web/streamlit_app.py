import streamlit as st
from src.config.settings import load_config
from src.api.client import (
    check_api_health,
    get_api_providers,
    call_api_summarize,
    call_api_chat
)

def main():
    config = load_config()
    
    st.set_page_config(
        page_title=config["ui"]["page_title"],
        page_icon=config["ui"]["page_icon"],
        layout=config["ui"]["layout"]
    )
    
    st.markdown("""
    <style>
    .topic-highlight {
        background: linear-gradient(90deg, #f0f2f6, #e8eaf6);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        color: #333333 !important;
        font-weight: bold;
    }
    .summary-container {
        background: #fafafa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        color: #333333 !important;
        line-height: 1.6;
    }
    .stMarkdown h3 {
        color: #1f77b4 !important;
        margin-bottom: 0.5rem;
    }
    .topic-highlight * {
        color: #333333 !important;
    }
    .summary-container * {
        color: #333333 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📄 Webpage Summarizer")
    st.markdown("Enter a URL to get a concise summary of the webpage content.")
    
    if not check_api_health():
        st.error("❌ API server is not running. Please start the API first:")
        st.code("uv run python run_api.py")
        st.info("💡 Make sure the API server is running on port 8000 before using the web interface.")
        return
    
    providers_response = get_api_providers()
    if "error" in providers_response:
        st.error(f"❌ Error connecting to API: {providers_response['error']}")
        st.info("💡 Please make sure the API server is running and accessible.")
        return
    
    available_providers = providers_response.get("available_providers", {})
    
    if not available_providers:
        st.warning("⚠️ No API keys configured. The app will return mock responses.")
        st.info("📝 To use real AI models, add your API keys to the `.env` file")
        
        st.sidebar.header("⚙️ Configuration")
        st.sidebar.success("✅ API server connected")
        st.sidebar.info("🤖 Mock mode - no provider selection needed")
        selected_provider = None
        selected_model = None
    else:
        st.sidebar.header("⚙️ Configuration")
        st.sidebar.success("✅ API server connected")
        
        provider_names = list(available_providers.keys())
        selected_provider = st.sidebar.selectbox("Choose Provider", provider_names)
        
        provider_config = available_providers[selected_provider]
        models = provider_config["models"]
        default_model = provider_config["default_model"]
        
        selected_model = st.sidebar.selectbox(
            "Choose Model",
            models,
            index=models.index(default_model)
        )
    

    
    url = st.text_input("Enter URL to summarize:", placeholder="https://example.com/article")
    
    if st.button("🚀 Summarize", type="primary"):
        if not url:
            st.error("Please enter a URL")
            return
        
        with st.spinner("Processing..."):
            result = call_api_summarize(url, selected_provider, selected_model)
            
            if "error" in result:
                st.error(result["error"])
                return
            
            st.success("✅ Analysis complete!")
            
            if "session_id" in result:
                st.session_state.current_session_id = result["session_id"]
                st.session_state.current_topic = result["main_topic"]
                st.session_state.current_summary = result["summary"]
                
                st.session_state.persistent_summary = result["summary"]
                st.session_state.persistent_topic = result["main_topic"]
                
                st.success("✅ Analysis complete! Summary is now available below for reference and chat.")
                            
            st.markdown("")
    
    if hasattr(st.session_state, 'current_session_id') and st.session_state.current_session_id:
        st.markdown("---")
        st.markdown("### 💬 **Chat with Summary**")
        st.info(f"💡 **Context:** {st.session_state.current_topic} - Ask questions about the content above")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("#### 📋 **Current Summary Context**")
        with col2:
            if "show_summary" not in st.session_state:
                st.session_state.show_summary = True
            show_summary = st.checkbox("Show Summary", value=st.session_state.show_summary, key="show_summary_checkbox")
            st.session_state.show_summary = show_summary
        
        if show_summary:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="topic-highlight"><strong>Topic: {st.session_state.current_topic}</strong></div>', 
                           unsafe_allow_html=True)
            with col2:
                if st.button("📋 Copy Summary", key="copy_summary_btn"):
                    st.write("Summary copied to clipboard!")
                    st.session_state.copied = True
                    st.rerun()
            
            st.markdown(f'<div class="summary-container">{st.session_state.current_summary}</div>', 
                       unsafe_allow_html=True)
        else:
            st.info("📋 Summary is hidden. Check the box above to show it again.")
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        st.markdown("**💡 Quick Reference:** " + st.session_state.current_topic)
        
        with st.form("chat_form", clear_on_submit=True):
            user_question = st.text_input(
                "Ask a question about the summary:",
                placeholder="What are the main points? Can you elaborate on...?"
            )
            submitted = st.form_submit_button("💬 Ask", type="primary")
            
            if submitted and user_question:
                with st.spinner("Thinking..."):
                    chat_result = call_api_chat(st.session_state.current_session_id, user_question)
                    
                    if "error" in chat_result:
                        st.error(f"Chat error: {chat_result['error']}")
                    else:
                        st.session_state.chat_history.append((user_question, chat_result["answer"]))
                        st.rerun()
        
        if st.session_state.chat_history:
            st.markdown("#### 💭 **Conversation History**")
            for i, (question, answer) in enumerate(st.session_state.chat_history):
                with st.container():
                    st.markdown(f"**🙋 You:** {question}")
                    st.markdown(f"**🤖 Assistant:** {answer}")
                    if i < len(st.session_state.chat_history) - 1:
                        st.markdown("---")
        
        if st.session_state.chat_history:
            if st.button("🔄 Clear Chat History", type="secondary"):
                st.session_state.chat_history = []
                st.rerun()
    
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666;">Built with ❤️ using Streamlit and FastAPI</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
