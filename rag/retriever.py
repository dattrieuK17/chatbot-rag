from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from langchain_chroma import Chroma
from chromadb import Settings
from rag.rewriter import rewrite_query

# ==== Embedding Model ====
class CustomSentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_id='AITeamVN/Vietnamese_Embedding'):
        self.model = SentenceTransformer(model_id, trust_remote_code=True)

    def embed_documents(self, texts):
        return self.model.encode(texts, convert_to_tensor=False).tolist()

    def embed_query(self, text):
        return self.model.encode([text], convert_to_tensor=False)[0].tolist()

def create_doc_from_chunk(diem_chunks):
    documents_with_context = []
    for chunk in diem_chunks:
        full_text = ""
        if chunk.get("dieu"):
            full_text += f"{chunk['dieu']}\n"
        if chunk.get("khoan"):
            full_text += f"{chunk['khoan']}\n"
        full_text += chunk["content"]

        documents_with_context.append(
            Document(page_content=full_text, metadata={
                "chuong": chunk.get("chuong", ""),
                "muc": chunk.get("muc", ""),
                "dieu": chunk.get("dieu", ""),
                "khoan": chunk.get("khoan", ""),
            })
        )
    return documents_with_context

def create_db(documents_with_context):
    """
    Tạo cơ sở dữ liệu Chroma từ danh sách các tài liệu.
    """
    # Tạo cơ sở dữ liệu Chroma
    client_settings = Settings(
        persist_directory="chroma_db_new",
        is_persistent=True,
    )

    chroma_db = Chroma.from_documents(
        documents=documents_with_context,
        embedding=CustomSentenceTransformerEmbeddings(),
        client_settings=client_settings,
    )

def load_db():
    client_settings = Settings(
        persist_directory="D:\chatbot_rag\chroma_db_new",
        is_persistent=True,
    )

    db = Chroma(
        persist_directory="chroma_db_new",
        embedding_function=CustomSentenceTransformerEmbeddings(),
        client_settings=client_settings,
    )
    return db

def retrieve_documents(chroma_db, query, k=4):
    """
    Truy xuất các tài liệu từ cơ sở dữ liệu Chroma dựa trên truy vấn.
    """
    rewritten_query = rewrite_query(query)
    print(rewritten_query)
    
    return chroma_db.as_retriever(search_kwargs={"k": k}).invoke(rewritten_query)