import requests

def inference(rewritten_query, docs):
    """
    Hàm này thực hiện truy vấn đến Groq API để lấy câu trả lời cho câu hỏi dựa trên ngữ cảnh đã cho.
    
    Args:
        rewritten_query (str): Câu hỏi đã được viết lại.
        docs (list): Danh sách các tài liệu chứa ngữ cảnh liên quan.
    
    Returns:
        str: Câu trả lời từ mô hình.
    """

    # Thay thế bằng API Key của bạn trên Groq
    API_KEY = "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"

    # Chọn mô hình phù hợp
    MODEL = "deepseek-r1-distill-llama-70b" 

    # Các đoạn văn bản liên quan
    context_1, context_2, context_3, context_4 = [doc.page_content for doc in docs]

    # Tạo prompt cho mô hình
    prompt = f"""Bạn là trợ lý pháp lý thông minh. Dựa trên ngữ cảnh sau, hãy trả lời câu hỏi một cách ngắn gọn và chính xác. Nếu không đủ thông tin, hãy nói rõ.

    Ngữ cảnh: Được lấy từ nghị định 168
    {context_1}
    {context_2}
    {context_3}
    {context_4}

    Câu hỏi: {rewritten_query}

    Trả lời:"""

    # Cấu hình yêu cầu đến Groq API
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Bạn là trợ lý pháp lý thông minh."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "top_p": 1.0,
        "stream": False
    }

    # Gửi yêu cầu và xử lý phản hồi
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        answer = result['choices'][0]['message']['content'].strip()
        return answer
    else:
        return "Error: " + response.text
