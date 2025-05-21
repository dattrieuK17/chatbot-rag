import torch

torch.backends.cuda.enable_flash_sdp(False)
torch.backends.cuda.enable_math_sdp(True)

import warnings
warnings.filterwarnings("ignore")

from rag.retriever import load_db, retrieve_documents
from rag.inferencer import inference
from rag.rewriter import rewrite_query


db = load_db()

def rag_chain(query):
    """
    Hàm này thực hiện quy trình RAG: viết lại truy vấn, truy xuất tài liệu và suy diễn.
    
    Args:
        query (str): Câu hỏi đầu vào.
        
    Returns:
        str: Câu trả lời từ mô hình.
    """
    # Viết lại truy vấn
    rewritten_query = rewrite_query(query)
    
    # Truy xuất tài liệu
    context_docs = retrieve_documents(db, rewritten_query, k=4)
    
    # Suy diễn
    answer = inference(rewritten_query, context_docs)
    
    return answer


if __name__ == "__main__":
    # Ví dụ câu hỏi
    query = input("Nhập câu hỏi của bạn: ")
    
    # Thực hiện quy trình RAG
    answer = rag_chain(query)
    
    print("Câu hỏi:", query)
    print("Câu trả lời:", answer)