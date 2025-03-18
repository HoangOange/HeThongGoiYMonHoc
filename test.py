from deep_translator import GoogleTranslator

text = "Introduction to Data Science"
translated_text = GoogleTranslator(source='auto', target='vi').translate(text)

print(translated_text)  # Nếu hoạt động, nó sẽ in: "Giới thiệu về Khoa học Dữ liệu"