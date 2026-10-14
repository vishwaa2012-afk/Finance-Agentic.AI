from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

def create_llm():
    return ChatOllama(
        model="llama3.2:3b",
        temperature=0,
        num_predict=1200,
    )

if __name__ == "__main__":
    llm = create_llm()
    res = llm.invoke("Hello, are you working?")
    print("\n--- LLM Output ---")
    print(res.content)
    