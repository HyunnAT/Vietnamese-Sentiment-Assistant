Vietnamese Sentiment Assistant (PhoBERT)

1. Giới thiệu
   Vietnamese Sentiment Assistant là ứng dụng phân tích cảm xúc tiếng Việt dựa trên mô hình Transformer PhoBERT. Hệ thống cho phép người dùng nhập văn bản tiếng Việt và nhận kết quả phân loại cảm xúc ở ba mức: Positive, Neutral và Negative.

2. Mục tiêu dự án
- Chuẩn hóa và xử lý các biến thể tiếng Việt như viết tắt và văn bản không dấu.
- Lưu trữ kết quả phân tích dưới dạng cơ sở dữ liệu cục bộ SQLite.
- Thiết kế giao diện web đơn giản, hiện đại và dễ sử dụng.
- Phân loại đung 3 nhan cảm xuc: POSITIVE, NEUTRAL, NEGATIVE.
- Hiểu các biến thể tiếng Việt (viết tắt, thiếu dấu).
- Độ chính xác phân loại: ≥ 65% trên 10 test case.

3. Tính năng chính
- Phân tích cảm xúc: Tiếp nhận câu tiếng Việt tự do, tiền xử lý văn bản, áp dụng mô hình PhoBERT để phân loại cảm xúc, trả về nhãn cảm xúc và điểm tin cậy (score).
- Lưu trữ lịch sử: Lưu văn bản, nhãn cảm xúc, điểm số và thời gian phân tích, sử dụng cơ sở dữ liệu SQLite và truy vấn theo thứ tự thời gian. Hiển thị lại lịch sử phân tích theo dạng bảng.
- Giao diện người dùng: Giao diện chạy bằng Streamlit, sử dụng tab để phân chia khu vực chức năng (phân tích / lịch sử). Trình bày kết quả rõ ràng, có màu sắc trực quan tùy theo nhãn cảm xúc.
4. Công nghệ sử dụng
- Ngôn ngữ lập trình: Python 3.9+
- Mô hình NLP: PhoBERT – wonrax/phobert-base-vietnamese-sentiment
- Thư viện NLP: HuggingFace Transformers
- Tiền xử lý tiếng Việt: underthesea + chuẩn hóa tùy chỉnh
- Giao diện: Streamlit
- Cơ sở dữ liệu: SQLite
- Xử lý dữ liệu:pandas
5. Cài đặt
- Tải python phiên bản 3.10 trở lên
- Bước 1. Tạo môi trường ảo:
   - python -m venv venv
   - venv\Scripts\activate (Windows)
- Bước 2. Cài đặt thư viện: pip install -r requirements.txt
- Bước 3. Chạy ứng dụng: streamlit run app.py
