import re

# Kiểm tra xem underthesea có được cài đặt không
try:
    from underthesea import word_tokenize
    HAS_UNDERTHESEA = True
except ImportError:
    HAS_UNDERTHESEA = False

# Từ viết tắt phổ biến trong tiếng Việt
ABBREVIATIONS = {
    "ko": "không","k": "không","kh": "không",
    "dc": "được","vs": "với","mn": "mọi người",
    "hnay": "hôm nay","tks": "cảm ơn",
    "zui": "vui", "j": "gì", "bùn": "buồn",
    "thik": "thích", "r": "rồi",
    "cx": "cũng","hok": "không",
}

# Chuẩn hóa văn bản
def normalize(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


# Mở rộng từ viết tắt
def expand_abbrev(text: str) -> str:
    words = text.split()
    new_words = []
    for w in words:
        lw = w.lower()
        if lw in ABBREVIATIONS:
            new_words.append(ABBREVIATIONS[lw])
        else:
            new_words.append(w)
    return " ".join(new_words)

# Tách từ (word segmentation)
def segment(text: str) -> str:
    """
    PhoBERT hoạt động tốt hơn nếu text đã word-segmented.
    Nếu không có underthesea thì trả nguyên văn.
    """
    if not HAS_UNDERTHESEA:
        return text
    return word_tokenize(text, format="text")

# Tổng hợp các bước tiền xử lý
def preprocess_text(text: str) -> str:
    if not text:
        return ""
    text = normalize(text)
    text = expand_abbrev(text)
    text = segment(text)
    # Cắt bớt cho nhẹ
    return text[:200]
