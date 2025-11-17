import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import minmax_scale

# ====== 파일 경로 설정 ======
file_path = r'C:\\Users\\KJG\\Desktop\\불용어전처리완)중복제거Top5_키워드_Dataset.csv'  # 분석할 CSV 파일
stopwords_file_path = r'C:\\Users\\KJG\\Desktop\\additional_stopwords.xlsx'  # 불용어 목록 엑셀 파일
output_path = r'C:\\Users\\KJG\\Desktop\\top20_tfidf_keywords.csv'  # 결과 저장 경로

# ====== CSV 파일 로드 ======
max_columns = 5059  # 데이터의 최대 열 수
column_names = [f'col_{i}' for i in range(max_columns)]
data = pd.read_csv(
    file_path,
    header=None,
    names=column_names,
    on_bad_lines='skip',
    low_memory=False,
    dtype=str
)

# ====== 텍스트 결합 ======
# 한 행(row)을 하나의 문서로 간주하고, 모든 셀 내용을 공백으로 결합
data['combined_text'] = data.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

# ====== 불용어 목록 로드 ======
try:
    stopwords_data = pd.read_excel(stopwords_file_path, header=None)
    stopwords_list = stopwords_data[0].dropna().tolist()
except Exception as e:
    print(f"⚠️ 불용어 파일을 불러오는 중 오류 발생: {e}")
    stopwords_list = []

# ====== TF-IDF 계산 ======
print("🔍 TF-IDF 계산 중...")
vectorizer = TfidfVectorizer(stop_words=stopwords_list)
tfidf_matrix = vectorizer.fit_transform(data['combined_text'])

# 각 단어의 평균 TF-IDF 점수 계산
tfidf_scores = tfidf_matrix.mean(axis=0).tolist()[0]
terms = vectorizer.get_feature_names_out()
term_scores = list(zip(terms, tfidf_scores))

# TF-IDF 점수를 기준으로 내림차순 정렬
sorted_terms = sorted(term_scores, key=lambda x: x[1], reverse=True)

# 상위 20개 키워드 선택 및 정규화
top_20_terms = sorted_terms[:20]
top_20_keywords = pd.DataFrame(top_20_terms, columns=["Keyword", "TF-IDF Score"])
top_20_keywords["Scaled TF-IDF Score"] = minmax_scale(top_20_keywords["TF-IDF Score"], feature_range=(0, 1))

# ====== 결과 저장 ======
top_20_keywords.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"✅ TF-IDF 상위 20개 키워드가 '{output_path}'에 저장되었습니다.")
