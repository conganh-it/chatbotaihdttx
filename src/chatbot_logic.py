import os
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
# Thêm các import sau cho PromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from config import LLM_TEMPERATURE, OLLAMA_LLM_MODEL
from src.embedding_and_storage import get_vector_db
from config import VECTOR_DB_DIR

def initialize_chatbot():
    vectorstore = get_vector_db(VECTOR_DB_DIR)
    if vectorstore is None:
        print("Không thể tải cơ sở dữ liệu vector. Chatbot không thể khởi tạo.")
        return None

    print(f"Đang tải mô hình LLM từ Ollama: {OLLAMA_LLM_MODEL}")
    try:
        llm = ChatOllama(model=OLLAMA_LLM_MODEL, temperature=LLM_TEMPERATURE)
        llm.invoke("Xin chào, bạn là ai?") # Kiểm tra kết nối
        print("Mô hình Ollama LLM đã được tải và kết nối thành công.")
    except Exception as e:
        print(f"Lỗi khi tải hoặc kết nối với mô hình Ollama LLM '{OLLAMA_LLM_MODEL}': {e}")
        print("Vui lòng đảm bảo Ollama đang chạy và bạn đã 'ollama pull' mô hình này.")
        return None

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    print("Retriever đã được cấu hình.")

    # --- PHẦN THAY ĐỔI ĐỂ CHATBOT TRẢ LỜI TIẾNG VIỆT ---

    # Định nghĩa template cho prompt
    # Chúng ta thêm hướng dẫn "Hãy trả lời bằng tiếng Việt." vào đây.
    template = """Sử dụng các đoạn văn bản ngữ cảnh sau đây để trả lời câu hỏi ở cuối.
    Nếu bạn không biết câu trả lời, hãy nói rằng bạn không biết, đừng cố bịa ra câu trả lời.
    Hãy trả lời bằng tiếng Việt.

    {context}

    Câu hỏi: {question}
    Trả lời tiếng Việt:"""

    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # Tạo chuỗi RetrievalQA với prompt tùy chỉnh
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT} # Truyền prompt tùy chỉnh vào đây
    )
    # --- KẾT THÚC PHẦN THAY ĐỔI ---

    print("Chuỗi chatbot RetrievalQA đã được khởi tạo thành công.")
    return qa_chain

def get_chatbot_response(qa_chain, query: str):
    # ... (giữ nguyên hàm này) ...
    if qa_chain is None:
        return {"answer": "Chatbot chưa được khởi tạo. Vui lòng kiểm tra lỗi trước đó.", "sources": []}

    try:
        response = qa_chain.invoke({"query": query})
        answer = response["result"]
        source_documents = response.get("source_documents", [])

        sources_info = []
        for doc in source_documents:
            source = doc.metadata.get("source", "Không rõ file")
            page = doc.metadata.get("page", None)

            source_display = f"{os.path.basename(source)}"
            if page is not None:
                source_display += f", Trang: {page}"

            sources_info.append(source_display)

        unique_sources = list(set(sources_info))

        return {
            "answer": answer,
            "sources": unique_sources
        }
    except Exception as e:
        print(f"Lỗi khi lấy câu trả lời từ chatbot: {e}")
        return {"answer": "Xin lỗi, đã có lỗi xảy ra khi xử lý yêu cầu của bạn. Vui lòng thử lại sau.", "sources": []}

if __name__ == "__main__":
    # ... (giữ nguyên phần kiểm thử) ...
    print("--- Chạy kiểm thử module chatbot_logic ---")
    qa_chain_test = initialize_chatbot()
    if qa_chain_test:
        print("\nChatbot đã sẵn sàng cho kiểm thử.")
        test_query = input("Nhập một câu hỏi để kiểm tra (ví dụ: 'Sales data trong quý 1 là gì?'): ")
        response_test = get_chatbot_response(qa_chain_test, test_query)
        print(f"\nChatbot: {response_test['answer']}")
        if response_test['sources']:
            print("Nguồn tham khảo:")
            for source in response_test['sources']:
                print(f"- {source}")
    else:
        print("Không thể kiểm thử chatbot do lỗi khởi tạo.")