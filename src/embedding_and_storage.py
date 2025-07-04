import os
from langchain_community.embeddings import HuggingFaceEmbeddings  # Sử dụng cho Sentence Transformers
from langchain_community.vectorstores import Chroma
from config import EMBEDDING_MODEL_NAME, VECTOR_DB_DIR
from src.data_processing import load_documents_from_directory, split_documents_into_chunks


def create_and_save_vector_db(documents_dir: str, vector_db_dir: str):
    """
    Tải tài liệu, chia nhỏ, tạo embeddings (biểu diễn số của văn bản)
    và lưu trữ chúng vào cơ sở dữ liệu vector ChromaDB.
    """
    # 1. Tải tài liệu từ thư mục nguồn
    documents = load_documents_from_directory(documents_dir)
    if not documents:
        print("Không có tài liệu nào để xử lý. Vui lòng thêm file vào thư mục 'data/documents'.")
        return None

    # 2. Chia nhỏ tài liệu thành các đoạn văn bản (chunks)
    chunks = split_documents_into_chunks(documents)
    if not chunks:
        print("Không có đoạn văn bản nào được tạo từ tài liệu.")
        return None

    # 3. Khởi tạo mô hình nhúng (Embedding Model)
    # Chúng ta sử dụng HuggingFaceEmbeddings để tải mô hình Sentence Transformer
    # đã chỉ định trong config.py.
    print(f"Đang tải mô hình nhúng: {EMBEDDING_MODEL_NAME}")
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        print("Mô hình nhúng đã được tải thành công.")
    except Exception as e:
        print(f"Lỗi khi tải mô hình nhúng '{EMBEDDING_MODEL_NAME}': {e}")
        print("Vui lòng kiểm tra kết nối internet và tên mô hình.")
        print("Đảm bảo bạn đã cài đặt 'sentence-transformers' trong requirements.txt.")
        return None

    # 4. Tạo và lưu VectorStore vào đĩa
    print(f"Đang tạo và lưu trữ cơ sở dữ liệu vector tại: {vector_db_dir}...")
    try:
        # Chroma.from_documents sẽ tạo embeddings từ các chunks và lưu vào thư mục
        vectorstore = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory=vector_db_dir  # Chỉ định thư mục lưu trữ
        )
        print("Cơ sở dữ liệu vector đã được tạo và lưu thành công.")
        return vectorstore
    except Exception as e:
        print(f"Lỗi khi tạo hoặc lưu cơ sở dữ liệu vector: {e}")
        return None


def get_vector_db(vector_db_dir: str):
    """
    Tải cơ sở dữ liệu vector từ thư mục đã lưu.
    Hàm này được dùng khi cơ sở dữ liệu đã được tạo trước đó,
    giúp tránh việc phải xử lý lại tài liệu mỗi lần chạy bot.
    """
    # Kiểm tra xem thư mục lưu trữ ChromaDB có tồn tại không
    # File 'chroma.sqlite3' là một dấu hiệu tốt cho thấy DB đã được khởi tạo
    chroma_db_path = os.path.join(vector_db_dir, "chroma.sqlite3")
    if not os.path.exists(chroma_db_path):
        print(f"Cơ sở dữ liệu vector chưa được tìm thấy tại '{vector_db_dir}'.")
        print("Vui lòng chạy lại chương trình để tạo hoặc đảm bảo có file trong 'data/documents'.")
        return None

    # Khởi tạo lại mô hình nhúng để Chroma có thể đọc lại các embedding
    print(f"Đang tải mô hình nhúng để kết nối với cơ sở dữ liệu vector: {EMBEDDING_MODEL_NAME}")
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    except Exception as e:
        print(f"Lỗi khi tải mô hình nhúng '{EMBEDDING_MODEL_NAME}': {e}")
        print("Không thể tải cơ sở dữ liệu vector mà không có mô hình nhúng phù hợp.")
        return None

    print(f"Đang tải cơ sở dữ liệu vector từ: {vector_db_dir}...")
    try:
        vectorstore = Chroma(persist_directory=vector_db_dir, embedding_function=embeddings)
        print("Cơ sở dữ liệu vector đã được tải thành công.")
        return vectorstore
    except Exception as e:
        print(f"Lỗi khi tải cơ sở dữ liệu vector từ '{vector_db_dir}': {e}")
        return None


# Chỉ chạy phần này khi file được chạy trực tiếp (để kiểm tra)
if __name__ == "__main__":
    print("--- Chạy kiểm thử module embedding_and_storage ---")

    # Bước 1: Tạo và lưu DB (chỉ cần chạy lần đầu hoặc khi có dữ liệu mới)
    print("\nĐang thử tạo và lưu cơ sở dữ liệu vector...")
    created_vectorstore = create_and_save_vector_db(DOCUMENTS_DIR, VECTOR_DB_DIR)

    if created_vectorstore:
        print("\nĐã tạo thành công DB. Đang thử tải lại DB...")
        # Bước 2: Tải lại DB để kiểm tra
        loaded_vectorstore = get_vector_db(VECTOR_DB_DIR)
        if loaded_vectorstore:
            print("Tải lại DB thành công. Bạn có thể tiếp tục với logic chatbot.")
        else:
            print("Lỗi khi tải lại DB.")
    else:
        print("Không thể tạo DB. Vui lòng kiểm tra các lỗi trên.")