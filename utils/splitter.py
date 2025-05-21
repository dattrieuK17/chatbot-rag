import re

def split_by_chuong_from_documents(documents):
    """
    Tách văn bản từ danh sách documents theo CHƯƠNG.
    Trả về danh sách dict gồm 'chuong' và 'content'.
    """
    
    # Gộp toàn bộ văn bản sau khi làm sạch
    full_text = "\n".join([doc.page_content for doc in documents])
    
    # Tách theo CHƯƠNG
    pattern = r"(Chương\s+[IVXLC]+\s*\n[^\n]*)"
    parts = re.split(pattern, full_text)
    
    chuong_chunks = []
    for i in range(1, len(parts), 2):
        chuong_title = parts[i].strip()
        chuong_content = parts[i+1].strip() if i+1 < len(parts) else ""
        chuong_chunks.append({
            "chuong": chuong_title,
            "content": chuong_content
        })
    
    return chuong_chunks

def split_by_muc(chuong_chunks):
    """
    Tách mỗi chương thành các mục theo định dạng 'Mục 1. TIÊU ĐỀ'.
    Nếu chương không có mục, toàn bộ nội dung sẽ nằm trong mục None.
    """
    all_muc_chunks = []
    pattern = r"(Mục\s+\d+\.\s*[^\n]*)"  # Mục 1. ..., Mục 2. ...

    for chuong in chuong_chunks:
        content = chuong["content"]
        parts = re.split(pattern, content)

        if len(parts) == 1:
            # Không có Mục trong chương
            all_muc_chunks.append({
                "chuong": chuong["chuong"],
                "muc": None,
                "content": parts[0].strip()
            })
        else:
            for i in range(1, len(parts), 2):
                muc_title = parts[i].strip()
                muc_content = parts[i+1].strip() if i+1 < len(parts) else ""
                all_muc_chunks.append({
                    "chuong": chuong["chuong"],
                    "muc": muc_title,
                    "content": muc_content
                })

    return all_muc_chunks

def split_by_dieu(muc_chunks):
    """
    Tách từng mục/chương thành các Điều.
    Lấy đúng tiêu đề của điều, kể cả khi tiêu đề xuống dòng, không kết thúc bằng dấu chấm.
    """
    all_dieu_chunks = []
    pattern = r"(?m)^Điều\s+\d+\..*"

    for muc in muc_chunks:
        content = muc["content"]
        matches = list(re.finditer(pattern, content))

        if not matches:
            continue  # Không có điều nào

        for i in range(len(matches)):
            start = matches[i].start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            full_text = content[start:end].strip()

            # Ghép dòng đầu tiên (hoặc nhiều dòng đầu tiên) thành tiêu đề cho đến khi gặp dòng trắng hoặc dòng bắt đầu bằng số/khoản
            lines = full_text.split('\n')
            title_lines = []
            body_lines = []
            found_body = False

            for line in lines:
                if not found_body and (
                    re.match(r"^\s*\d+\.", line) or  # bắt đầu khoản
                    re.match(r"^\s*[a-zA-Z]\)", line) or  # bắt đầu điểm
                    line.strip() == ""
                ):
                    found_body = True
                if not found_body:
                    title_lines.append(line.strip())
                else:
                    body_lines.append(line.strip())

            dieu_title = " ".join(title_lines).strip()
            dieu_body = "\n".join(body_lines).strip()

            all_dieu_chunks.append({
                "chuong": muc["chuong"],
                "muc": muc["muc"],
                "dieu": dieu_title,
                "content": dieu_body
            })

    return all_dieu_chunks

def split_by_khoan(dieu_chunks):
    """
    Tách từng điều thành các Khoản.
    Giữ đúng tiêu đề của Khoản kể cả khi tiêu đề xuống dòng và không có dấu chấm.
    """
    all_khoan_chunks = []
    pattern = r"(?m)^\s*\d+\..*"

    for dieu in dieu_chunks:
        content = dieu["content"]
        matches = list(re.finditer(pattern, content))

        if not matches:
            # Không có Khoản, coi toàn bộ nội dung là 1 Khoản không định danh
            all_khoan_chunks.append({
                "chuong": dieu["chuong"],
                "muc": dieu["muc"],
                "dieu": dieu["dieu"],
                "khoan": None,
                "content": content.strip()
            })
            continue

        for i in range(len(matches)):
            start = matches[i].start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            full_text = content[start:end].strip()

            # Ghép các dòng đầu để tạo title khoản
            lines = full_text.split('\n')
            title_lines = []
            body_lines = []
            found_body = False

            for line in lines:
                if not found_body and (
                    re.match(r"^\s*[a-zA-Z]\)", line) or  # điểm
                    line.strip() == ""  # dòng trắng
                ):
                    found_body = True
                if not found_body:
                    title_lines.append(line.strip())
                else:
                    body_lines.append(line.strip())

            khoan_title = " ".join(title_lines).strip()
            khoan_body = "\n".join(body_lines).strip()

            all_khoan_chunks.append({
                "chuong": dieu["chuong"],
                "muc": dieu["muc"],
                "dieu": dieu["dieu"],
                "khoan": khoan_title,
                "content": khoan_body
            })

    return all_khoan_chunks

def split_by_diem_dynamic_length(khoan_chunks, max_length=1000):
    """
    Gộp các điểm trong mỗi Khoản thành nhiều chunk sao cho mỗi chunk không vượt quá max_length ký tự.
    """
    all_diem_chunks = []
    pattern = r"(?m)^[a-z]\)"  # điểm bắt đầu bằng a), b), ...

    for khoan in khoan_chunks:
        content = khoan["content"]
        matches = list(re.finditer(pattern, content))

        # Nếu không có điểm nào, giữ nguyên nội dung
        if not matches:
            all_diem_chunks.append({
                "chuong": khoan["chuong"],
                "muc": khoan["muc"],
                "dieu": khoan["dieu"],
                "khoan": khoan["khoan"],
                "content": content.strip()
            })
            continue

        # Cắt từng điểm riêng biệt
        diem_texts = []
        for i in range(len(matches)):
            start = matches[i].start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            diem_text = content[start:end].strip()
            diem_texts.append(diem_text)

        # Gom nhóm điểm sao cho mỗi nhóm không vượt quá max_length
        current_chunk = ""
        for diem in diem_texts:
            if len(current_chunk) + len(diem) + 1 > max_length:
                if current_chunk:
                    all_diem_chunks.append({
                        "chuong": khoan["chuong"],
                        "muc": khoan["muc"],
                        "dieu": khoan["dieu"],
                        "khoan": khoan["khoan"],
                        "content": current_chunk.strip()
                    })
                current_chunk = diem
            else:
                current_chunk += "\n" + diem if current_chunk else diem

        # Thêm chunk cuối nếu còn dư
        if current_chunk:
            all_diem_chunks.append({
                "chuong": khoan["chuong"],
                "muc": khoan["muc"],
                "dieu": khoan["dieu"],
                "khoan": khoan["khoan"],
                "content": current_chunk.strip()
            })

    return all_diem_chunks

