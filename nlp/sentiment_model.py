from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from .preprocess import preprocess_text

MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"

_tokenizer = None
_model = None
_sentiment_pipeline = None

# Bản đồ nhãn từ mô hình sang nhãn chuẩn
LABEL_MAPPING = {
    "POS": "POSITIVE",
    "NEG": "NEGATIVE",
    "NEU": "NEUTRAL",
}

# Các từ/ cụm từ để bổ sung luật phân loại
NEG_WORDS = [
    "buc minh", "bực mình", "buc minh qua", "bực mình quá",
    "te", "tệ", "qua te", "quá tệ",
    "chan", "chán", "that vong", "thất vọng",
    "ko dc", "không được", "thảm hại", "kinh khung", "ket xe", "kẹt xe"
]

POS_WORDS = [
    "rat vui", "rất vui", "vui ve", "vui vẻ", "cuc ky vui ve", "cực kỳ vui", "cực kỳ vui vẻ","vui",
    "ngon", "ngon tuyet voi", "ngon tuyệt vời","rat ngon",
    "tuyet voi", "tuyệt vời", "thich", "thích",
    "tot", "tốt", "than thien", "thân thiện"
]

NEUTRAL_HINTS = [
    "hom nay", "hôm nay", "hnay",
    "mai", "ngay mai",
    "bay gio", "bây giờ", "bay gio la", "bây giờ là",
    "gio chieu", "giờ chiều",
    "di lam", "đi làm",
    "dang ngoi", "đang ngồi",
    "lam bai tap", "làm bài tập",
    "thu hai", "thứ hai"
]

def _contains_any(text_lower: str, patterns) -> bool:
    return any(p in text_lower for p in patterns)

# Lazy load PhoBERT pipeline
def _get_pipeline():
    """Lazy load PhoBERT lần đầu, các lần sau dùng lại."""
    global _tokenizer, _model, _sentiment_pipeline

    if _sentiment_pipeline is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=_model,
            tokenizer=_tokenizer
        )
    return _sentiment_pipeline

# Hàm phân tích cảm xúc
def analyze_sentiment(raw_text: str) -> dict:
    if raw_text is None or raw_text.strip() == "":
        return {"text": raw_text, "sentiment": "NEUTRAL", "score": 0.0}

    clean_text = preprocess_text(raw_text)
    text_lower = clean_text.lower()

    # 1. Gọi PhoBERT (lazy)
    pipe = _get_pipeline()
    result = pipe(clean_text)[0]

    label_raw = result.get("label", "NEU")
    score = float(result.get("score", 0.0))
    mapped_label = LABEL_MAPPING.get(label_raw, "NEUTRAL")

    # 2. Luật bổ sung dựa trên từ khóa
    if _contains_any(text_lower, NEG_WORDS):
        mapped_label = "NEGATIVE"

    if _contains_any(text_lower, POS_WORDS):
        mapped_label = "POSITIVE"

    if (not _contains_any(text_lower, NEG_WORDS)
            and not _contains_any(text_lower, POS_WORDS)
            and _contains_any(text_lower, NEUTRAL_HINTS)):
        mapped_label = "NEUTRAL"

    if score < 0.55:
        mapped_label = "NEUTRAL"

    return {
        "text": raw_text,
        "sentiment": mapped_label,
        "score": score
    }
