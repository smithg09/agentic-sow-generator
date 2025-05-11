from config import OPENAI_API_KEY, AZURE_API_BASE_URL, AZURE_TEXT_EMBEDDING, AZURE_EMBEDDING_URL_PATH, POSTGRESQL_BASE_URL, EMBEDDING_COL_NAME
from langchain_postgres import PGVector
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.documents import Document
import uuid

class VectorService:
    def __init__(self):
        self.embeddings = AzureOpenAIEmbeddings(
            model=AZURE_TEXT_EMBEDDING,
            azure_endpoint=f"{AZURE_API_BASE_URL}{AZURE_EMBEDDING_URL_PATH}",
            api_key=OPENAI_API_KEY,
            openai_api_version="2023-05-15",
        )

        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=EMBEDDING_COL_NAME,
            connection=f"postgresql+psycopg://{POSTGRESQL_BASE_URL}",
            use_jsonb=True,
        )

        # Querying embeddings 
        self.retriever = self.vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 2})
    
    def retrieve_context(self, query):
        """Retrieve relevant context from vector store based on query"""
        return self.retriever.invoke(query)
    
    def store_document(self, content, file_name="user_generated_sow"):
        """Store a document in the vector database"""
        doc = Document(
            page_content=content,
            metadata={"id": str(uuid.uuid4()), "fileName": file_name},
        )
        
        self.vector_store.add_documents([doc], ids=[doc.metadata["id"]])
        return doc.metadata["id"]

# Initialize vector service as a singleton
vector_service = VectorService()