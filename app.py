from flask import Flask, request, jsonify, render_template
import torch
import warnings
import re

# Tối ưu torch nếu cần
torch.backends.cuda.enable_flash_sdp(False)
torch.backends.cuda.enable_math_sdp(True)
warnings.filterwarnings("ignore")

# Import RAG pipeline
from rag.retriever import load_db, retrieve_documents
from rag.inferencer import inference
from rag.rewriter import rewrite_query

# Load database 1 lần khi khởi động
db = load_db()

app = Flask(__name__)

# Trang giao diện chính
@app.route("/")
def index():
    return render_template("app.html")

# API xử lý chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("message", "").strip()
    
    if not query:
        return jsonify({"reply": "Vui lòng nhập câu hỏi."}), 400

    try:
        rewritten_query = rewrite_query(query)
        context_docs = retrieve_documents(db, rewritten_query, k=4)
        answer = inference(rewritten_query, context_docs)
        cleaned_answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
        return jsonify({"reply": cleaned_answer})
    except Exception as e:
        return jsonify({"reply": f"Đã xảy ra lỗi: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
