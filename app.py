import streamlit as st
import pandas as pd

from nlp.sentiment_model import analyze_sentiment
from storage.db import Database

# Configure Streamlit page
st.set_page_config(
    page_title="Vietnamese Sentiment Assistant",
    layout="wide",
    page_icon="📈"
)

db = Database("sentiments.db")

# Load custom CSS
try:
    with open("static/style.css", "r", encoding="utf-8") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Header
st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
st.markdown("""
<div class="header">
    <div class="app-title">Vietnamese Sentiment Assistant (PhoBERT)</div>
    <div class="app-subtitle">
        Phân tích cảm xúc tiếng Việt bằng mô hình Transformer PhoBERT &amp; lưu trữ SQLite.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# Tabs
tab_analyze, tab_history = st.tabs(["💬 Phân tích cảm xúc", "📑 Lịch sử phân tích"])

# Tab 1: Phân tích cảm xúc
with tab_analyze:
    st.write("") 

    user_text = st.text_area(
        "Nhập câu tiếng Việt:",
        placeholder="Ví dụ: Hôm nay tôi rất vui vì được đi học.",
        height=170
    )

    analyze_clicked = st.button("Phân loại cảm xúc", key="analyze_btn")

    if "last_result" not in st.session_state:
        st.session_state["last_result"] = None

    if analyze_clicked:
        if not user_text or len(user_text.strip()) < 12:
            st.warning("⚠️ Câu quá ngắn, hãy nhập ít nhất 12 ký tự.")
        else:
            with st.spinner("Đang phân tích bằng PhoBERT..."):
                result = analyze_sentiment(user_text)
                db.insert_sentiment(result["text"], result["sentiment"], result["score"])
                st.session_state["last_result"] = result

    last = st.session_state["last_result"]

    # Hiển thị kết quả phân tích gần nhất
    if last:
        sent = last["sentiment"]
        score = last["score"]

        icon = {"POSITIVE": "😊", "NEGATIVE": "😞", "NEUTRAL": "😐"}[sent]
        css_class = {
            "POSITIVE": "result-positive",
            "NEGATIVE": "result-negative",
            "NEUTRAL": "result-neutral"
        }[sent]

        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-badge {css_class}">
                    <span class="badge-icon">{icon}</span>
                    <span class="badge-text">{sent}</span>
                    <span class="badge-score">score={score:.3f}</span>
                </div>
                <div class="result-text">
                    <b>Câu đầu vào:</b> {last["text"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Tab 2: Lịch sử phân tích
with tab_history:
    st.write("")
    history = db.get_history(limit=20)

    if history:
        df = pd.DataFrame(history)
        df.columns = ["Nội dung", "Cảm xúc", "Score", "Thời gian"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.markdown(
            """
            <div class="empty-history">
                Chưa có bản ghi nào. Hãy thử phân tích một câu.
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)  # end page-wrapper
