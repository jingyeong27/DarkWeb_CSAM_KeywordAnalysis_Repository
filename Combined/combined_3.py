import pandas as pd
import numpy as np
import networkx as nx
from sklearn.preprocessing import minmax_scale
from gensim.models import Word2Vec
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from tqdm import tqdm
import operator
import os

# 사용자 정의 불용어 목록을 엑셀에서 읽어오는 함수
def load_additional_stopwords(excel_file):
    try:
        df = pd.read_excel(excel_file)
        additional_stopwords = set(df.iloc[:, 0].dropna().str.lower().tolist())
        return additional_stopwords
    except Exception as e:
        print(f"불용어 목록을 엑셀에서 불러오는 중 오류 발생: {e}")
        return set()

# 텍스트 전처리 함수
def process_line(line, stop_words, tokenizer, additional_stopwords):
    count = {}
    words = line.lower()
    tokens = tokenizer.tokenize(words)
    stopped_tokens = [i for i in set(tokens) if i not in stop_words and i not in additional_stopwords and len(i) > 1]
    for i, a in enumerate(stopped_tokens):
        for b in stopped_tokens[i+1:]:
            count[(min(a, b), max(a, b))] = count.get((min(a, b), max(a, b)), 0) + 1
    return count

# 고유벡터 중심성 계산 함수
def calculate_eigenvector_centrality(lines_pos, stop_words, tokenizer, additional_stopwords):
    combined_count = {}
    # 멀티스레딩 대신 순차적으로 처리
    for line in tqdm(lines_pos, desc="동시출현 빈도 계산 진행률"):
        result = process_line(line, stop_words, tokenizer, additional_stopwords)
        for key, value in result.items():
            combined_count[key] = combined_count.get(key, 0) + value

    G_pos = nx.Graph()
    for (term1, term2), freq in combined_count.items():
        if freq > 10:
            G_pos.add_edge(term1, term2, weight=freq)

    egv = nx.eigenvector_centrality(G_pos, max_iter=1000, tol=1e-06)
    sorted_egv = sorted(egv.items(), key=operator.itemgetter(1), reverse=True)
    egv_df = pd.DataFrame(sorted_egv[:20], columns=['Eigen Keyword', 'Eigenvector Score'])
    egv_df["Scaled Eigenvector Score"] = minmax_scale(egv_df['Eigenvector Score'])

    return egv_df

# Word2Vec 모델 학습 및 고유 키워드 추출 함수
def calculate_word2vec(lines_pos, stop_words, tokenizer, additional_stopwords):
    text = []
    for line in lines_pos:
        words = line.lower()
        tokens = tokenizer.tokenize(words)
        stopped_tokens = [i for i in set(tokens) if i not in stop_words and i not in additional_stopwords and len(i) > 1]
        text.append(stopped_tokens)

    # Word2Vec 모델 생성 시 seed 값을 설정하여 결과를 재현 가능하게 함
    model = Word2Vec(text, sg=1, window=3, min_count=10, seed=42)
    return model

# 고유벡터와 Word2Vec 고유 키워드 조합 계산 및 저장
def calculate_and_save_combinations(eigen_df, model, output_path):
    eigen_keywords = set(eigen_df['Eigen Keyword'])
    w2v_keywords = {word for word in model.wv.index_to_key if word not in eigen_keywords}

    combined_keywords = []
    for _, eigen_row in eigen_df.iterrows():
        for word in w2v_keywords:
            similarity_score = model.wv.similarity(eigen_row['Eigen Keyword'], word)
            combined_score = eigen_row['Scaled Eigenvector Score'] + similarity_score
            combined_keywords.append({
                'Eigen Keyword': eigen_row['Eigen Keyword'],
                'Eigenvector Score': eigen_row['Eigenvector Score'],
                'Scaled Eigenvector Score': eigen_row['Scaled Eigenvector Score'],
                'Word2Vec Keyword': word,
                'Similarity Score': similarity_score,
                'Combined Score': combined_score
            })

    combined_df = pd.DataFrame(combined_keywords)
    combined_df['Scaled Similarity Score'] = minmax_scale(combined_df['Similarity Score'])
    combined_df.to_csv(output_path, index=False)
    print(f"조합 결과가 {output_path}에 저장되었습니다.")

# 파일 경로 및 설정
file_path = 'C:\\Users\\KJG\\Desktop\\child_sex_crimes_keywords.csv'  # 실제 파일 경로 사용
stopwords_file_path = 'C:\\Users\\KJG\\Desktop\\additional_stopwords.xlsx'  # 불용어 파일 경로 사용
output_path = 'C:\\Users\\KJG\\Desktop\\Eigen+word2vec_combined_3_keywords_scores.csv'

# 파일 경로 존재 확인
if not os.path.exists(file_path):
    raise FileNotFoundError(f"파일 경로가 잘못되었습니다: {file_path}")
if not os.path.exists(stopwords_file_path):
    raise FileNotFoundError(f"불용어 파일 경로가 잘못되었습니다: {stopwords_file_path}")

# 데이터 로드 및 전처리
try:
    data = pd.read_csv(file_path, header=None, dtype=str, sep=',', on_bad_lines='skip', names=[f'col_{i}' for i in range(5059)])
    data['combined_text'] = data.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
except Exception as e:
    print(f"CSV 파일을 로드하는 중 오류가 발생했습니다: {e}")

# 불용어 로드 및 토크나이저 설정
additional_stopwords = load_additional_stopwords(stopwords_file_path)
stop_words = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')

# 고유벡터 계산
eigen_df = calculate_eigenvector_centrality(data['combined_text'], stop_words, tokenizer, additional_stopwords)

# Word2Vec 모델 학습 및 고유 키워드 추출
model = calculate_word2vec(data['combined_text'], stop_words, tokenizer, additional_stopwords)

# 조합 결과 계산 및 CSV로 저장
calculate_and_save_combinations(eigen_df, model, output_path)
