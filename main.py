import os
import sys
from src.embedding_and_storage import create_and_save_vector_db, get_vector_db
from src.chatbot_logic import initialize_chatbot, get_chatbot_response
from config import DOCUMENTS_DIR, VECTOR_DB_DIR, OLLAMA_LLM_MODEL
from dotenv import load_dotenv


def main():
    # Tải biến môi trường (nếu có, dù ở đây không dùng)
    load_dotenv()

    # 1. Đảm bảo các thư mục cần thiết tồn tại
    print("Đang kiểm tra và tạo các thư mục dự án...")
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    print("Các thư mục đã sẵn sàng.")

    # 2. Kiểm tra và tạo/cập nhật Vector DB
    # Một cách để kiểm tra sự tồn tại của ChromaDB là tìm file 'chroma.sqlite3'
    chroma_db_exists = os.path.exists(os.path.join(VECTOR_DB_DIR, "chroma.sqlite3"))

    if not chroma_db_exists:
        print("\nCơ sở dữ liệu vector chưa tồn tại hoặc cần cập nhật.")
        print("Đang tiến hành tải tài liệu, tạo embedding và lưu vào cơ sở dữ liệu...")
        vectorstore_ready = create_and_save_vector_db(DOCUMENTS_DIR, VECTOR_DB_DIR)
        if not vectorstore_ready:
            print(
                "Không thể tạo hoặc tải cơ sở dữ liệu vector. Vui lòng kiểm tra lỗi và đảm bảo có tài liệu trong 'data/documents'.")
            sys.exit(1)  # Thoát nếu không thể tạo DB
    else:
        print("\nCơ sở dữ liệu vector đã tồn tại. Đang tải từ bộ nhớ...")
        # Cố gắng tải lại để đảm bảo không có vấn đề gì
        vectorstore_ready = get_vector_db(VECTOR_DB_DIR)
        if not vectorstore_ready:
            print(
                "Lỗi khi tải cơ sở dữ liệu vector. Có thể cơ sở dữ liệu bị hỏng. Hãy thử xóa 'data/vector_db' và chạy lại.")
            sys.exit(1)  # Thoát nếu không thể tải DB

    # 3. Khởi tạo chatbot
    print(f"\nĐang khởi tạo chatbot với mô hình Ollama: {OLLAMA_LLM_MODEL}...")
    qa_chain = initialize_chatbot()
    if qa_chain is None:
        print("Không thể khởi tạo chatbot. Vui lòng kiểm tra các lỗi trên và đảm bảo Ollama đang chạy.")
        sys.exit(1)  # Thoát nếu không khởi tạo được chatbot

    print("\n--- Chatbot đã sẵn sàng! ---")
    print("Bạn có thể bắt đầu trò chuyện. Gõ 'exit' hoặc 'thoat' để kết thúc.")

    # 4. Vòng lặp trò chuyện chính
    while True:
        user_query = input("\nBạn: ")
        if user_query.lower() in ["exit", "thoat"]:
            print("Chatbot: Tạm biệt! Hẹn gặp lại bạn.")
            break

        # Lấy câu trả lời từ chatbot
        response = get_chatbot_response(qa_chain, user_query)
        print(f"Chatbot: {response['answer']}")

        # Hiển thị nguồn tham khảo (nếu có)
        if response['sources']:
            print("Nguồn tham khảo:")
            for source in response['sources']:
                print(f"- {source}")


if __name__ == "__main__":
    main()