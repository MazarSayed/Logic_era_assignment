from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from models import StructuredSummary
from src.config.settings import load_prompts

def summarize_content(content, llm):
    print(f"🤖 Summarizing {len(content)} characters with structured output")
    
    prompts = load_prompts()
    parser = PydanticOutputParser(pydantic_object=StructuredSummary)
    
    system_prompt = prompts["summarize"]["system"] + f"\n\n{parser.get_format_instructions()}"
    user_prompt = f"Content: {content}"
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    try:
        response = llm.invoke(messages)
        
        if hasattr(response, 'content'):
            response_text = response.content
        elif hasattr(response, 'text'):
            response_text = response.text
        else:
            response_text = str(response)
        
        print(f"✅ LLM response received: {len(response_text)} characters")
        print(f"📝 Response preview: {response_text[:200]}...")
        
        result = parser.parse(response_text)
        
        print(f"✅ Structured output successful - Topic: {result.topic}")
        return result.summary, result.topic
        
    except Exception as e:
        print(f"⚠️ Structured output failed: {e}")
        try:
            import json
            if "```json" in response_text:
                json_part = response_text.split("```json")[1].split("```")[0].strip()
            elif "{" in response_text and "}" in response_text:
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                json_part = response_text[start:end]
            else:
                json_part = response_text.strip()
            
            parsed = json.loads(json_part)
            summary = parsed.get("summary", "")
            topic = parsed.get("topic", "")
            
            if summary and topic:
                print(f"✅ Manual JSON parsing successful - Topic: {topic}")
                return summary, topic
            else:
                raise ValueError("Missing summary or topic in response")
                
        except Exception as e2:
            print(f"⚠️ Manual JSON parsing also failed: {e2}")
            return content, "Content Analysis"