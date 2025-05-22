from google import genai

def rewrite_query(user_query):
    
    client = genai.Client(api_key="")
    
    prompt = f"""
    Bạn là một chuyên gia pháp lý, am hiểu sâu sắc về văn bản quy phạm pháp luật.
    
    Nhiệm vụ của bạn là chuyển đổi câu hỏi của người dân thành một truy vấn phù hợp với phong cách hành chính – pháp lý, bảo đảm:
    - Văn phong trang trọng, chính xác, không sử dụng đại từ nhân xưng (tôi, bạn...).
    - Câu văn ngắn gọn, mạch lạc, theo cấu trúc ngôn ngữ pháp lý chuẩn.
    - Làm rõ chủ thể, hành vi và mối quan hệ với quy định trong nghị định.
    - Không thêm thông tin không có trong câu hỏi gốc.
    
    Ví dụ:
    Câu hỏi gốc: "Vượt đèn đỏ bị phạt bao nhiêu tiền?"
    Câu hỏi pháp lý: Mức phạt tiền đối với hành vi vi phạm vượt đèn tín hiệu giao thông khi đèn đang ở trạng thái đỏ được quy định như thế nào?
    
    Câu hỏi gốc: "Hành vi đi ngược chiều sẽ bị xử phạt như thế nào?"
    Câu hỏi pháp lý: "Mức xử phạt vi phạm hành chính đối với hành vi điều khiển phương tiện giao thông đi ngược chiều được quy định như thế nào theo pháp luật hiện hành?"
    
    Câu hỏi gốc: "{user_query}"
    Hãy viết lại câu hỏi này theo văn phong của văn bản pháp luật.
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    
    return response.text