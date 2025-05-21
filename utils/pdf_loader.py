from langchain.document_loaders import PyPDFLoader
import re
from langchain.schema import Document


def clean_text(doc):
    """
    Nhận một đối tượng Document có thuộc tính page_content.
    Làm sạch nội dung văn bản bằng cách:
    - Xoá "about:blank"
    - Xoá chuỗi ngày giờ định sẵn "5/15/25, 8:43 PM"
    - Loại bỏ khoảng trắng thừa
    """
    text = doc.page_content
    text = re.sub(r'about:blank', '', text)
    text = re.sub(r'5/15/25, 8:43 PM', '', text)
    doc.page_content = text.strip()
    return doc

def load_pdf(file_path: str) -> list[Document]:
    """
    Load a PDF file and return a list of Document objects.
    
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        list[Document]: A list of Document objects.
    """
    # Load the PDF file
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Clean the text in each document
    documents = [clean_text(doc) for doc in documents]

    return documents