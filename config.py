import os
from dotenv import load_dotenv

load_dotenv() # Tải các biến môi trường từ file .env (ở đây thì không có gì)

# Paths
DOCUMENTS_DIR = "data/documents"
VECTOR_DB_DIR = "data/vector_db"

# Embedding settings
# Sử dụng mô hình từ Sentence Transformers. "paraphrase-multilingual-MiniLM-L12-v2"
# là một lựa chọn tốt vì hỗ trợ tiếng Việt và khá nhẹ.
# Bạn cũng có thể dùng "intfloat/multilingual-e5-large" nếu muốn embedding tốt hơn (nặng hơn).
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# LLM settings (sử dụng Ollama)
OLLAMA_LLM_MODEL = "mistral" # Đảm bảo bạn đã 'ollama pull mistral'
# Nếu bạn pull mô hình khác, thay đổi tên ở đây, ví dụ: "llama2", "phi3"
LLM_TEMPERATURE = 0.7 # Điều chỉnh độ "sáng tạo" của bot (0.0 - 1.0)

# Chunking settings
CHUNK_SIZE = 1000 # Kích thước mỗi đoạn văn bản
CHUNK_OVERLAP = 200 # Số ký tự chồng lấp giữa các đoạn