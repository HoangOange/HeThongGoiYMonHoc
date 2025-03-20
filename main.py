import os
import pickle
import streamlit as st
from deep_translator import GoogleTranslator

# Thiết lập CSS để thay đổi màu nền & chữ
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        color: white;
    }
    h2, h3, h4, h5, h6, p, label, div {
        color: black !important;
        text-align: center;
    }
    .stButton button {
        background-color: #0044cc;
        color: white;
        border-radius: 10px;
        padding: 8px 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load dữ liệu
courses_list = pickle.load(open('models/courses.pkl', 'rb'))
similarity = pickle.load(open('models/similarity.pkl', 'rb'))

# Hàm gợi ý môn học
def recommend(course):
    index = courses_list[courses_list['course_name'] == course].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_courses = [(courses_list.iloc[i[0]].course_name, courses_list.iloc[i[0]].course_link) for i in distances[1:7]]
    return recommended_courses

# Tạo đối tượng dịch sang tiếng Việt
translator = GoogleTranslator(source="auto", target="vi")

# Giao diện tiêu đề
st.markdown("<h2>Hệ thống gợi ý môn học - Nhóm 10</h2>", unsafe_allow_html=True)

# Chọn khóa học
selected_course = st.selectbox("🔎 Nhập hoặc chọn môn học bạn thích:", courses_list['course_name'].values)

# Dịch khóa học được chọn
translated_course = translator.translate(selected_course)
st.write(f"📖 **Tên khóa học dịch:** {translated_course}")

# Hiển thị các môn học gợi ý
if st.button("🎯 Hiện các môn học gợi ý"):
    recommended_courses = recommend(selected_course)
    st.write("📌 **Những môn học mà bạn có thể thích:**")
    
    for course_name, course_link in recommended_courses:
        translated_course = translator.translate(course_name)
        st.markdown(f'<p style="color:black; font-size:16px;">📘 <a href="{course_link}" target="_blank" style="color:black; text-decoration:none;"><b>{translated_course}</b></a></p>', unsafe_allow_html=True)

