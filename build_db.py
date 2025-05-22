from utils.splitter import split_by_chuong_from_documents, split_by_muc, split_by_dieu, split_by_khoan, split_by_diem_dynamic_length
from utils.pdf_loader import load_pdf
from rag.retriever import create_db, create_doc_from_chunk


def build_db(file_path: str):
    """
    Hàm này xây dựng cơ sở dữ liệu từ file PDF.
    
    Args:
        file_path (str): Đường dẫn đến file PDF.
        
    Returns:
        None
    """
    # Load the PDF file
    documents = load_pdf(file_path)

    # Split the documents into chunks
    chuong_chunks = split_by_chuong_from_documents(documents)
    muc_chunks = split_by_muc(chuong_chunks)
    dieu_chunks = split_by_dieu(muc_chunks)
    khoan_chunks = split_by_khoan(dieu_chunks)
    diem_chunks = split_by_diem_dynamic_length(khoan_chunks)

    # Create the database
    documents_with_context = create_doc_from_chunk(diem_chunks)
    db = create_db(documents_with_context)

    return db

if __name__ == "__main__":
    # Đường dẫn đến file PDF
    file_path = "data/nghidinh-168.pdf"
    
    # Xây dựng cơ sở dữ liệu
    build_db(file_path)

    print("Cơ sở dữ liệu đã được xây dựng thành công.")