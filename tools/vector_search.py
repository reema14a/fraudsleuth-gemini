from google import genai
from google.genai import types

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

from config.config import EMBEDDING_MODEL, GEMINI_API_KEY, CHROMA_COLLECTION_NAME
import os

client = genai.Client(api_key=GEMINI_API_KEY)


# for m in client.models.list():
#     if "embedContent" in m.supported_actions:
#         print(m.name)

#model_name = "gemini-2.0-flash"


class GeminiEmbeddingFunction(EmbeddingFunction):
    # Specify whether to generate embeddings for documents, or queries
    def __init__(self, document_mode=True):
        self.document_mode = document_mode

    def __call__(self, input: Documents) -> Embeddings:
        if self.document_mode:
            embedding_task = "retrieval_document"
        else:
            embedding_task = "retrieval_query"

        
        response = client.models.embed_content(
                                    model = EMBEDDING_MODEL,
                                    contents = input,
                                    config = types.EmbedContentConfig(
                                        task_type = embedding_task,
                                    )
                                )
        
        # Return list of embedding vectors
        return [e.values for e in response.embeddings]
        

class ChromaVectorSearch:

    def __init__(self, persist_directory="chroma_db", collection_name = CHROMA_COLLECTION_NAME):
        
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path = self.persist_directory)
        self.embed_fn = GeminiEmbeddingFunction(document_mode = True)
    
        # Create or get collection
        self.collection = self.client.get_or_create_collection(name = self.collection_name,
                                                               embedding_function = self.embed_fn)
        
        self.load_documents_from_file("data/knowledge_base.txt")

    def load_documents_from_file(self, file_path: str):
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                docs = [line.strip() for line in f if line.strip()]
                self.add_documents(docs)
                print(f"✅ Loaded {len(docs)} documents from {file_path} into ChromaDB.")
        else:
            print(f"⚠️ File not found: {file_path}")

    def add_documents(self, documents: list[str], ids: list[str] = None):
        """
        Adds documents to ChromaDB with embeddings.
        """
        if not documents:
            print("⚠️ No documents to add.")
            return
        if ids is None:
            ids = [str(i) for i in range(len(documents))]
        self.collection.add(documents = documents, ids = ids)

    def query(self, text: str, n_results: int = 5):
        """
        Queries the collection for top matching documents.
        """

        results = self.collection.query(query_texts=[text], n_results = n_results)
        return results

    def reset_collection(self):
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(name = self.collection_name, 
                                                               embedding_function = self.embed_fn)

