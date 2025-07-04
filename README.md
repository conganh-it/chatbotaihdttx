# Chatbot AI Hỏi Đáp Từ Tài Liệu Cục Bộ

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Tính năng chính](#tính-năng-chính)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
  - [1. Cài đặt Ollama](#1-cài-đặt-ollama)
  - [2. Kéo mô hình LLM](#2-kéo-mô-hình-llm)
  - [3. Thiết lập môi trường Python](#3-thiết-lập-môi-trường-python)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Sử dụng](#sử-dụng)
- [Cấu hình](#cấu-hình)
- [Khắc phục sự cố](#khắc-phục-sự-cố)
- [Đóng góp](#đóng-góp)
- [Giấy phép](#giấy-phép)

## Giới thiệu

🤖 Chatbot AI trả lời câu hỏi tự động dựa trên nội dung tài liệu Word, PDF, Excel cục bộ.

Sử dụng Ollama (chạy LLM local), LangChain và FAISS/ChromaDB để xử lý tịnh huống, tìm kiếm đoạn văn, trích xuất thông tin.

## Tính năng chính
- 🔍 **Hỏi đáp từ tài liệu**: Word/PDF/Excel
- 💡 **Xử lý ngôn ngữ tiếng Việt**
- 📁 **Chạy hoàn toàn cục bộ**, không dùng GPT/API
- 📄 **Trích dẫn nguồn tham chiếu**

## Yêu cầu hệ thống
- Hệ điều hành: Windows/macOS/Linux
- Python >= 3.9
- RAM >= 8GB
- Dung lượng trống: 3–5GB

## Cài đặt

### 1. Cài đặt Ollama
- https://ollama.com/
- Tải và cài theo hệ điều hành

### 2. Kéo mô hình
```bash
ollama pull mistral
```

### 3. Thiết lập Python
```bash
python -m venv .venv
source .venv/bin/activate  # hoặc .venv\Scripts\activate
pip install -r requirements.txt
```

## Cấu trúc dự án
```
your_chatbot_project/
├── data/
│   ├── documents/         # Tài liệu nguồn (.pdf, .docx, .xlsx)
│   └── vector_db/         # Vector FAISS / ChromaDB
├── src/
│   ├── data_processing.py
│   ├── embedding_and_storage.py
│   └── chatbot_logic.py
├── main.py                # Điểm khởi chạy
├── config.py              # Tối ưu tham số
├── requirements.txt
├── .env
└── README.md
```

## Sử dụng
1. Đặt file vào `data/documents/`
2. Chạy index:
```bash
python src/embedding_and_storage.py
```
3. Chạy chatbot:
```bash
python main.py
```

## Cấu hình (config.py)
- `DOCUMENTS_DIR`, `VECTOR_DB_DIR`
- `EMBEDDING_MODEL_NAME`
- `OLLAMA_LLM_MODEL`: "mistral"
- `CHUNK_SIZE`, `CHUNK_OVERLAP`

## Khắc phục sự cố
- `ModuleNotFoundError`: Thiếu gói → `pip install -r requirements.txt`
- `ConnectionRefused`: Ollama chưa chạy hoặc chưa pull model
- Trả lời không đúng: Kiểm tra ngôn ngữ dữ liệu, chia chunk

## Đóng góp
Hoan nghênh PR, issue, góp týnh năng hay dataset mớ rộng chatbot.

## Giấy phép
Mã nguồn mở MIT
