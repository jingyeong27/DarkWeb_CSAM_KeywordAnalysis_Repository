import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import minmax_scale

# 파일 경로 및 설정
file_path = r'C:\\Users\\KJG\\Desktop\\불용어전처리완)중복제거Top5_키워드_Dataset.csv'  # 실제 파일 경로 사용
stopwords_file_path = r'C:\\Users\\KJG\\Desktop\\additional_stopwords.xlsx'  # 불용어 파일 경로 사용
eigenvector_result_path = r'C:\\Users\\KJG\\Desktop\\eigenvector_result.csv'  # 업로드된 고유벡터 중심성 결과 파일 경로

# 최대 열 개수 고정 (5059) 및 CSV 파일 로드
max_columns = 5059
column_names = [f'col_{i}' for i in range(max_columns)]
data = pd.read_csv(file_path, header=None, names=column_names, on_bad_lines='skip', low_memory=False, dtype=str)

# 모든 텍스트를 하나의 컬럼으로 결합 (각 행을 하나의 문서로 간주)
data['combined_text'] = data.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

# 불용어 리스트 로드 (엑셀 파일에서 불용어 목록 불러오기)
stopwords_data = pd.read_excel(stopwords_file_path, header=None)
stopwords_list = stopwords_data[0].tolist()  # 불용어를 리스트로 변환

# TF-IDF 계산 (불용어 적용)
vectorizer = TfidfVectorizer(stop_words=stopwords_list)
tfidf_matrix = vectorizer.fit_transform(data['combined_text'])

# 각 단어의 TF-IDF 점수를 평균하여 모든 키워드 추출
tfidf_scores = tfidf_matrix.mean(axis=0).tolist()[0]
terms = vectorizer.get_feature_names_out()
term_scores = list(zip(terms, tfidf_scores))
sorted_terms = sorted(term_scores, key=lambda x: x[1], reverse=True)

# 모든 TF-IDF 키워드 추출 후 DataFrame 생성
tfidf_keywords_df = pd.DataFrame(sorted_terms, columns=["TF-IDF Keyword", "TF-IDF Score"])

# 고유벡터 중심성 결과 파일 로드
eigen_df = pd.read_csv(eigenvector_result_path)

# 고유벡터 중심성 키워드와 겹치지 않는 TF-IDF 키워드 필터링
tfidf_only_keywords_df = tfidf_keywords_df[~tfidf_keywords_df['TF-IDF Keyword'].isin(eigen_df['eigen_keyword'])]

# Min-Max 스케일링 적용
tfidf_only_keywords_df["Scaled TF-IDF Score"] = minmax_scale(tfidf_only_keywords_df["TF-IDF Score"], feature_range=(0, 1))

# 고유벡터와 TF-IDF에만 존재하는 키워드의 조합 점수 계산 및 별도 CSV 저장
combined_keywords = []
if not eigen_df.empty:
    for _, eigen_row in eigen_df.iterrows():
        for _, tfidf_row in tfidf_only_keywords_df.iterrows():
            combined_score = eigen_row['eigen_minmax_score'] + tfidf_row['Scaled TF-IDF Score']
            combined_keywords.append({
                'Eigen Keyword': eigen_row['eigen_keyword'],
                'TF-IDF Only Keyword': tfidf_row['TF-IDF Keyword'],
                'Combined Score': combined_score
            })

    combined_df = pd.DataFrame(combined_keywords)
    combined_output_path = r'C:\\Users\\KJG\\Desktop\\Eigen+TF_IDFtotal_combined_2_keywords_scores.csv'
    combined_df.to_csv(combined_output_path, index=False)
    print("고유벡터와 TF-IDF에만 존재하는 키워드 조합 결과가 별도의 CSV 파일로 저장되었습니다:", combined_output_path)
