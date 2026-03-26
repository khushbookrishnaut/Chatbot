import json
import chromadb
from chromadb.utils import embedding_functions

def process_knowledge_base(file_path):
    print("1. Loading Knowledge Base...")
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    documents = []
    metadata_list = []
    ids = []
    
    for category in data['categories']:
        category_name = category['category_name']
        for item in category['items']:
            item_id = item.get('id', '')
            question = item.get('question', '')
            
            chunk_text = f"Category: {category_name}\nQuestion: {question}\n"
            if 'answer' in item: chunk_text += f"Answer: {item['answer']}\n"
            if 'details' in item:
                chunk_text += "Details:\n"
                for detail in item['details']: chunk_text += f"- {detail}\n"
            if 'steps' in item:
                chunk_text += "Steps to resolve:\n"
                for step in item['steps']: chunk_text += f"- {step}\n"
            if 'escalation_triggers' in item:
                chunk_text += "Escalation Triggers:\n"
                for trigger in item['escalation_triggers']: chunk_text += f"- {trigger}\n"
            
            documents.append(chunk_text.strip())
            metadata_list.append({"category": category_name})
            ids.append(item_id)
            
    return documents, metadata_list, ids

def create_database():
    print("2. Extracting Data...")
    docs, metadatas, ids = process_knowledge_base('knowledge_base.json')
    
    print("3. Setting up Chroma Database...")
    chroma_client = chromadb.PersistentClient(path="./agent_db")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = chroma_client.get_or_create_collection(
        name="aura_policies",
        embedding_function=sentence_transformer_ef
    )
    
    print("4. Saving chunks to database (This might take a minute the first time)...")
    collection.add(documents=docs, metadatas=metadatas, ids=ids)
    print("✅ Success! All data saved to ChromaDB successfully.")

if __name__ == "__main__":
    create_database()