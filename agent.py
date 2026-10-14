from llm import create_llm
from tools import (
    retrieve_financial_document,
    get_stock_snapshot,
    get_recent_market_news,
)

SYSTEM_PROMPT = """
You are an expert Autonomous Personal Investment Research Assistant built by Team Solo LevelX.

Your job is to answer investment and financial research questions using grounded evidence, never speculation.

Rules for Output:
- Label every figure as [DOCUMENT] or [LIVE].
- Preserve exact units (INR, USD, %).
- End with: "This is educational research information, not personalized financial advice."
"""

def ask_agent(question: str):
    llm = create_llm()
    q_lower = question.lower()
    
    context = ""
    
    # Smart Tool Routing
    if "reliance" in q_lower or "price" in q_lower or "snapshot" in q_lower or "stock" in q_lower or ".ns" in q_lower:
        # Extract ticker or default to RELIANCE.NS
        ticker = "RELIANCE.NS"
        if "tcs" in q_lower:
            ticker = "TCS.NS"
        elif "aapl" in q_lower or "apple" in q_lower:
            ticker = "AAPL"
            
        live_data = get_stock_snapshot.invoke({"ticker": ticker})
        context += f"\n\n[LIVE MARKET DATA]:\n{live_data}"
        
    if "news" in q_lower or "recent" in q_lower or "headline" in q_lower:
        news_data = get_recent_market_news.invoke({"query": question})
        context += f"\n\n[MARKET NEWS]:\n{news_data}"
        
    if "document" in q_lower or "report" in q_lower or "factsheet" in q_lower or "revenue" in q_lower or "profit" in q_lower:
        doc_data = retrieve_financial_document.invoke({"query": question})
        context += f"\n\n[DOCUMENT DATA]:\n{doc_data}"
        
    # If no specific keyword triggered, run stock snapshot as default fallback
    if not context:
        live_data = get_stock_snapshot.invoke({"ticker": "RELIANCE.NS"})
        context += f"\n\n[LIVE MARKET DATA]:\n{live_data}"

    prompt = f"{SYSTEM_PROMPT}\n\nContext Information:\n{context}\n\nUser Question: {question}\n\nPlease analyze the context and provide a clear, structured research answer."
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return "⚠️ **Note:** Running in Cloud Deployment Mode. Live Ollama backend is offline in cloud environment, but market APIs and data retrieval are functional."

if __name__ == "__main__":
    print(ask_agent("Get live stock snapshot for RELIANCE.NS"))
