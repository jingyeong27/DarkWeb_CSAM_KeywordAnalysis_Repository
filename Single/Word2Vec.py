import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from gensim.models import Word2Vec
from sklearn.preprocessing import minmax_scale
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import pymongo

# MongoDB 연결
def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Keywords_DB"]
    return db["Eigenvector_result"], db["Word2vec_result"]

# Word2Vec 모델 학습 함수
def calculate_word2vec(lines_pos, collection_centrality, collection_word2vec, additional_stopwords):
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('english'))

    text = []
    for line in lines_pos:
        tokens = tokenizer.tokenize(line.lower())
        filtered = [w for w in set(tokens) if w not in stop_words and w not in additional_stopwords and len(w) > 1]
        text.append(filtered)

    model = Word2Vec(text, sg=1, window=3, min_count=10)

    eigen_keywords = [d["eigen_keyword"] for d in collection_centrality.find({}, {"_id": 0, "eigen_keyword": 1})]
    all_pairs = {}

    def process_keyword(keyword):
        try:
            similar = model.wv.most_similar(keyword, topn=100)
            for word, score in similar:
                pair = tuple(sorted((keyword, word)))
                all_pairs[pair] = max(all_pairs.get(pair, 0), score)
        except KeyError:
            pass

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_keyword, kw) for kw in eigen_keywords]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Word2Vec 진행률"):
            pass

    scores = list(all_pairs.values())
    scaled_scores = minmax_scale(scores)

    for ((a, b), score), scaled in zip(all_pairs.items(), scaled_scores):
        doc = {
            "main_keyword": a,
            "related_keyword": b,
            "similarity_score": score,
            "word2vec_minmax_score": scaled
        }
        collection_word2vec.replace_one({"main_keyword": a, "related_keyword": b}, doc, upsert=True)

    print("✅ Word2Vec 결과 MongoDB 저장 완료.")

# 실행 예시
if __name__ == "__main__":
    coll_centrality, coll_word2vec = connect_to_mongo()
    file_path = r"C:\Users\KJG\Desktop\불용어전처리완)중복제거Top5_키워드_Dataset.csv"

    data = pd.read_csv(file_path, header=None, dtype=str, engine="python")
    data["combined_text"] = data.apply(lambda row: " ".join(row.dropna().astype(str)), axis=1)
    lines = data["combined_text"].tolist()

    additional_stopwords = {"www", "https", "darkweb"}
    calculate_word2vec(lines, coll_centrality, coll_word2vec, additional_stopwords)
