import os
import sys

# Thêm project root vào sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from nlp.sentiment_model import analyze_sentiment

# ===20 TEST CASE ===
# 1–10: Câu có dấu, chuẩn
# 11–20: Câu không dấu / viết tắt

TEST_CASES = [
    # Nhóm 1: Câu có dấu 
    {"text": "Hôm nay tôi rất vui.", "expected": "POSITIVE"},
    {"text": "Tôi thất vọng về kết quả.", "expected": "NEGATIVE"},
    {"text": "Trời không nắng cũng không mưa.", "expected": "NEUTRAL"},
    {"text": "Món ăn thật ngon tuyệt!", "expected": "POSITIVE"},
    {"text": "Dịch vụ quá tệ, tôi không hài lòng.", "expected": "NEGATIVE"},
    {"text": "Buổi học kết thúc lúc 10 giờ.", "expected": "NEUTRAL"},
    {"text": "Nhân viên phục vụ rất nhiệt tình.", "expected": "POSITIVE"},
    {"text": "Máy liên tục bị lỗi, bực mình thật.", "expected": "NEGATIVE"},
    {"text": "Ngày mai tôi đi làm từ 8 giờ sáng.", "expected": "NEUTRAL"},
    {"text": "Bộ phim này hay hơn tôi tưởng.", "expected": "POSITIVE"},

    # Nhóm 2: Không dấu + viết tắt
    # 4 câu tích cực
    {"text": "hom nay toi cuc ky vui ve", 
     "expected": "POSITIVE"},
    {"text": "mon an nay ngon tuyet voi, toi thich lam", 
     "expected": "POSITIVE"},
    {"text": "hnay di choi vs mn vui", 
     "expected": "POSITIVE"},
    {"text": "dich vu o day rat tot, nv than thien", 
     "expected": "POSITIVE"},

    # 4 câu tiêu cực
    {"text": "toii rat buc minh, that te, chan qua", 
     "expected": "NEGATIVE"},
    {"text": "quan nay phuc vu cha ra gi, that vong ghe", 
     "expected": "NEGATIVE"},
    {"text": "thi xong ma diem thap tham hai, buon muon khoc", 
     "expected": "NEGATIVE"},
    {"text": "hom nay bi ket xe kinh khung, di lam muon, buc minh qua", 
     "expected": "NEGATIVE"},

    # 2 câu trung tính (miêu tả thuần túy, không cảm xúc rõ)
    {"text": "hom nay la thu hai dau tuan", 
     "expected": "NEUTRAL"},
    {"text": "bay gio la 3 gio chieu, toi dang ngoi lam bai tap", 
     "expected": "NEUTRAL"},
]


def run_tests():
    correct = 0
    print("-KẾT QUẢ TEST 20 CÂU-\n")

    for i, tc in enumerate(TEST_CASES, start=1):
        res = analyze_sentiment(tc["text"])
        predicted = res["sentiment"]
        expected = tc["expected"]

        is_ok = (predicted == expected)
        if is_ok:
            correct += 1

        group = "Nhóm 1 (có dấu)" if i <= 10 else "Nhóm 2 (không dấu/viết tắt)"

        print(f"{i}. [{group}] {tc['text']}")
        print(f"   Mong đợi: {expected}")
        print(f"   Dự đoán : {predicted} (score={res['score']:.3f})")
        print(f"   Kết quả : {'ĐÚNG' if is_ok else 'SAI'}")
        print("-" * 70)

    acc = correct / len(TEST_CASES) * 100
    print(f"\nTổng số câu: {len(TEST_CASES)}")
    print(f"Số câu đúng: {correct}")
    print(f"Độ chính xác chung: {acc:.2f}%")

    if acc >= 65:
        print("=> ĐẠT yêu cầu >= 65%.")
    else:
        print("=> CHƯA đạt 65%, nên xem lại bộ test hoặc phân tích thêm.")
    

if __name__ == "__main__":
    run_tests()
