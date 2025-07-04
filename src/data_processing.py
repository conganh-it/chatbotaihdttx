import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import DOCUMENTS_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def load_documents_from_directory(directory_path: str):
    """
    Tải tất cả các tài liệu (PDF, DOCX, XLSX) từ một thư mục được chỉ định.
    Sử dụng các loader của LangChain để xử lý các định dạng file khác nhau.
    """
    all_documents = []
    print(f"Đang tải tài liệu từ thư mục: {directory_path}")

    # Kiểm tra xem thư mục có tồn tại không
    if not os.path.exists(directory_path):
        print(f"Lỗi: Thư mục '{directory_path}' không tồn tại. Vui lòng kiểm tra đường dẫn.")
        return []

    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):  # Chỉ xử lý các file, bỏ qua thư mục con
            if filename.lower().endswith(".pdf"):
                print(f"  Đang tải PDF: {filename}")
                loader = PyPDFLoader(filepath)
                all_documents.extend(loader.load())
            elif filename.lower().endswith(".docx"):
                print(f"  Đang tải DOCX: {filename}")
                # Docx2txtLoader đủ tốt cho văn bản, UnstructuredDocxLoader phức tạp hơn nhưng mạnh hơn
                loader = Docx2txtLoader(filepath)
                all_documents.extend(loader.load())
            elif filename.lower().endswith(".xlsx"):
                print(f"  Đang tải XLSX: {filename}")
                # UnstructuredExcelLoader giúp trích xuất nội dung từ bảng tốt hơn
                loader = UnstructuredExcelLoader(filepath)
                all_documents.extend(loader.load())
            else:
                print(f"  Bỏ qua file không được hỗ trợ: {filename}")

    if not all_documents:
        print(f"Không tìm thấy tài liệu nào trong thư mục: {directory_path}. Vui lòng thêm file vào.")
    else:
        print(f"Đã tải thành công {len(all_documents)} tài liệu.")

    return all_documents


def split_documents_into_chunks(documents):
    """
    Chia nhỏ các tài liệu đã tải thành các đoạn văn bản (chunks).
    Mỗi chunk có kích thước cố định và có thể có phần chồng lấp với chunk kế tiếp
    để đảm bảo ngữ cảnh không bị mất.
    """
    if not documents:
        print("Không có tài liệu nào để chia nhỏ.")
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,  # Hàm tính độ dài của chunk (theo ký tự)
        add_start_index=True,  # Thêm chỉ mục bắt đầu của chunk trong tài liệu gốc
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Đã chia {len(documents)} tài liệu thành {len(chunks)} đoạn văn bản (chunks).")
    return chunks


# Chỉ chạy phần này khi file được chạy trực tiếp (để kiểm tra)
if __name__ == "__main__":
    print(f"Thử nghiệm chức năng tải và chia nhỏ tài liệu từ: {DOCUMENTS_DIR}")
    docs = load_documents_from_directory(DOCUMENTS_DIR)
    if docs:
        chunks = split_documents_into_chunks(docs)
        if chunks:
            print("\n--- Ví dụ về một đoạn văn bản (Chunk đầu tiên) ---")
            print(f"Nội dung: {chunks[0].page_content[:300]}...")  # In 300 ký tự đầu tiên
            print(f"Nguồn: {chunks[0].metadata.get('source', 'Không rõ nguồn')}")
            print(f"Trang: {chunks[0].metadata.get('page', 'Không rõ trang')}")
            print(f"Start Index: {chunks[0].metadata.get('start_index', 'N/A')}")