import pickle
import time
from deep_translator import GoogleTranslator
import pandas as pd

# Load dữ liệu gốc
print("🔄 Đang tải dataset gốc...")
courses_list = pickle.load(open('models/courses.pkl', 'rb'))
print(f"✅ Đã tải {len(courses_list)} khóa học.")

# Hàm dịch với xử lý lỗi
def translate_text(text):
    try:
        translated = GoogleTranslator(source='auto', target='vi').translate(text)
        time.sleep(1)  # Dừng 1 giây để tránh bị Google chặn
        return translated
    except Exception as e:
        print(f"⚠️ Lỗi khi dịch: {text} - {e}")
        return text  # Trả về bản gốc nếu lỗi

print("🌍 Đang dịch khóa học sang tiếng Việt...")
courses_list['course_name_vi'] = courses_list['course_name'].apply(translate_text)

# Lưu lại dữ liệu đã dịch
pickle.dump(courses_list, open('models/courses_vi.pkl', 'wb'))
print("✅ Dataset đã được dịch và lưu thành 'models/courses_vi.pkl'")
