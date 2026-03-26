import requests
import json
import uuid
import chromadb
from chromadb.utils import embedding_functions

# 1. Database se connect karna
print("Loading Agent's Memory (ChromaDB)...")
chroma_client = chromadb.PersistentClient(path="./agent_db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_collection(name="aura_policies", embedding_function=sentence_transformer_ef)

# 2. Aapke Server ka address
URL = "http://localhost:5000/"
HEADERS = {"Content-Type": "application/json"}
SESSION_MEMORY_ID = str(uuid.uuid4())

print("\n" + "="*55)
print("🚀 Aura Electronics Smart Support Agent is LIVE!")
print("💡 Ask any policy question (Type 'exit' to quit)")
print("="*55 + "\n")

while True:
    # User se sawal lena
    user_input = input("You: ")
    
    if user_input.lower() in ['exit', 'quit']:
        print("Chat closed. Bye!")
        break

    # 3. DATABASE SEARCH: User ke sawal se milti-julti policy dhoondhna
    results = collection.query(
        query_texts=[user_input],
        n_results=2 # Top 2 sabse relevant chunks nikalna
    )
    
    # 4. Jo policy mili, usko text mein badalna
    retrieved_knowledge = "\n\n".join(results['documents'][0])
    
    # 5. THE MAGIC PROMPT (RAG): AI ko policy ke sath sawal bhejna
    smart_prompt = f"""You are a Customer Support Agent for Aura Electronics.
    Please answer the user's question using ONLY the knowledge base information provided below. 
    Keep your tone professional, empathetic, and concise. Do not make up information.
    
    --- KNOWLEDGE BASE INFO ---
    {retrieved_knowledge}
    ---------------------------
    
    User Question: {user_input}
    """

    # 6. Agent ko message bhejna
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {
                "messageId": str(uuid.uuid4()),
                "role": "user",
                "parts": [{"kind": "text", "text": smart_prompt}]
            },
            "contextId": SESSION_MEMORY_ID
        }
    }

    try:
        response = requests.post(URL, headers=HEADERS, json=payload)
        data = response.json()
        
        # Agent ka reply nikalna
        reply = data.get("result", {}).get("artifacts", [{}])[0].get("parts", [{}])[0].get("text", "Error in response")
        print(f"\nAgent: {reply}\n")
        
    except Exception as e:
        print(f"\n❌ Connection Error. Is your Docker server running? Error: {e}\n")