import pandas as pd
import numpy as np
import networkx as nx
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.preprocessing import minmax_scale
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import pymongo
import operator

# MongoDB 연결
def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Keywords_DB"]
    return db["Eigenvector_result"]

# 동시출현 단어쌍 계산 함수
def process_line(line, stop_words, tokenizer, additional_stopwords):
    count = {}
    words = line.lower()
    tokens = tokenizer.tokenize(words)
    stopped_tokens = [
        i for i in set(tokens)
        if i not in stop_words and i not in additional_stopwords and len(i) > 1
    ]
    for i, a in enumerate(stopped_tokens):
        for b in stopped_tokens[i + 1:]:
            key = tuple(sorted((a, b)))
            count[key] = count.get(key, 0) + 1
    return count

# 고유벡터 중심성 계산 함수
def calculate_eigenvector_centrality(lines_pos, collection_centrality, additional_stopwords):
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('english'))

    combined_count = {}
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_line, line, stop_words, tokenizer, additional_stopwords) for line in lines_pos]
        for future in tqdm(as_completed(futures), total=len(lines_pos), desc="동시출현 빈도 계산 진행률"):
            result = future.result()
            for key, value in result.items():
                combined_count[key] = combined_count.get(key, 0) + value

    df = pd.DataFrame.from_dict(combined_count, orient='index').reset_index()
    df[['term1', 'term2']] = pd.DataFrame(df['index'].tolist(), index=df.index)
    df.columns = ['pair', 'freq', 'term1', 'term2']
    df = df[df['freq'] > 10]

    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(row['term1'], row['term2'], weight=row['freq'])

    try:
        egv = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
    except nx.PowerIterationFailedConvergence:
        print("⚠️ 고유벡터 중심성 수렴 실패.")
        return

    sorted_egv = sorted(egv.items(), key=operator.itemgetter(1), reverse=True)
    egv_df = pd.DataFrame(sorted_egv[:20], columns=['Keyword', 'Eigenvector Score'])
    egv_df["Scaled Score"] = minmax_scale(egv_df["Eigenvector Score"])

    # MongoDB 저장
    for _, row in egv_df.iterrows():
        doc = {
            "eigen_keyword": row["Keyword"],
            "eigen_keyword_score": row["Eigenvector Score"],
            "eigen_minmax_score": row["Scaled Score"]
        }
        collection_centrality.replace_one({"eigen_keyword": row["Keyword"]}, doc, upsert=True)

    print("✅ 고유벡터 중심성 계산 및 MongoDB 저장 완료.")
    return egv_df

# 실행 예시
if __name__ == "__main__":
    collection = connect_to_mongo()
    file_path = r"C:\Users\KJG\Desktop\불용어전처리완)중복제거Top5_키워드_Dataset.csv"

    data = pd.read_csv(file_path, header=None, dtype=str, engine="python")
    data["combined_text"] = data.apply(lambda row: " ".join(row.dropna().astype(str)), axis=1)
    lines = data["combined_text"].tolist()

    additional_stopwords = {"www", "https", "darkweb"}
    calculate_eigenvector_centrality(lines, collection, additional_stopwords)
