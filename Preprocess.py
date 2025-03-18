import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

print('✅ Dependencies Imported')

# Đọc dữ liệu gốc
data = pd.read_csv("Data/Coursera.csv")
print(f"📂 Dữ liệu gốc có {data.shape[0]} khóa học và {data.shape[1]} cột")

# Kiểm tra thông tin dữ liệu
print("\n📊 Thông tin dữ liệu gốc:")
print(data.info())

# Kiểm tra dữ liệu bị thiếu
missing_values = data.isnull().sum()
print("\n🔍 Số lượng giá trị thiếu trên mỗi cột:")
print(missing_values[missing_values > 0])

# Chọn các cột quan trọng
data = data[['Course Name', 'Difficulty Level', 'Course Description', 'Skills']]

# Xử lý văn bản: Xóa ký tự đặc biệt và thay thế khoảng trắng
data['Course Name'] = data['Course Name'].str.replace(r'\s+', ' ', regex=True).str.strip()
data['Course Name'] = data['Course Name'].str.replace(':', '', regex=False)

data['Course Description'] = data['Course Description'].str.replace(r'\s+', ' ', regex=True).str.strip()
data['Course Description'] = data['Course Description'].str.replace('_', '', regex=False)
data['Course Description'] = data['Course Description'].str.replace(':', '', regex=False)
data['Course Description'] = data['Course Description'].str.replace(r'[()]', '', regex=True)

# Xóa dấu ngoặc tròn khỏi cột Skills
data['Skills'] = data['Skills'].str.replace(r'[()]', '', regex=True)

# Tạo cột tổng hợp tags
data['tags'] = data['Course Name'] + ' ' + data['Difficulty Level'] + ' ' + data['Course Description'] + ' ' + data['Skills']

# Đưa về chữ thường
data['tags'] = data['tags'].str.lower()

# Chuyển về dataframe mới chỉ gồm tên khóa học và tags
new_df = data[['Course Name', 'tags']].copy()
new_df.rename(columns={'Course Name': 'course_name'}, inplace=True)

# Loại bỏ dấu phẩy trong tên khóa học và tags
new_df['course_name'] = new_df['course_name'].str.replace(',', ' ', regex=False)
new_df['tags'] = new_df['tags'].str.replace(',', ' ', regex=False)

print("\n✅ Xử lý dữ liệu hoàn tất!")
print(new_df.head(10))  # In ra 10 dòng đầu tiên sau khi xử lý

# Xuất dữ liệu đã xử lý ra file CSV
output_csv_path = "processed_courses.csv"
new_df.to_csv(output_csv_path, index=False)
print(f"📤 Dữ liệu sau xử lý đã được lưu vào: {output_csv_path}")

# Mô hình hóa dữ liệu với Bag of Words
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

print("\n📈 Vector hóa hoàn tất! In thử vector đầu tiên:")
print(vectors[0])

# Stemming (Lemmatization)
import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
    return " ".join(ps.stem(word) for word in text.split())

new_df['tags'] = new_df['tags'].apply(stem)

# Tính toán độ tương đồng bằng Cosine Similarity
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

print("\n✅ Tính toán Cosine Similarity hoàn tất!")

# Lưu mô hình vào file
model_path = "models/"
os.makedirs(model_path, exist_ok=True)

pickle.dump(similarity, open(model_path + 'similarity.pkl', 'wb'))
pickle.dump(new_df.to_dict(), open(model_path + 'course_list.pkl', 'wb'))  # Chứa danh sách khóa học dưới dạng dict
pickle.dump(new_df, open(model_path + 'courses.pkl', 'wb'))  # Lưu toàn bộ dataframe đã xử lý

print("\n✅ Mô hình đã được lưu vào thư mục models/")
