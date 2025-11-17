import pymongo
from sklearn.preprocessing import minmax_scale

# 우선순위 계산 함수 (고유벡터 중심성과 Word2Vec 유사도 기반)
def calculate_keyword_priority(collection_centrality, collection_word2vec, collection_priority):
    try:
        # MongoDB에서 고유벡터 중심성 데이터 가져오기
        centrality_cursor = collection_centrality.find({}, {"eigen_keyword": 1, "eigen_minmax_score": 1})
        centrality_data = {doc["eigen_keyword"]: doc["eigen_minmax_score"] for doc in centrality_cursor}

        # MongoDB에서 Word2Vec 유사도 데이터 가져오기
        word2vec_cursor = collection_word2vec.find({}, {"main_keyword": 1, "related_keyword": 1, "word2vec_minmax_score": 1})

        # 우선순위 계산을 위한 키워드 페어 우선순위 계산
        priority_results = []
        seen_pairs = set()  # 중복 방지를 위한 키워드 페어 집합

        # 가중치 설정
        eigen_weight = 1
        w2v_weight = 1

        for doc in word2vec_cursor:
            main_keyword = doc["main_keyword"]
            related_keyword = doc["related_keyword"]
            w2v_score = doc["word2vec_minmax_score"]

            # 고유벡터 중심성 점수 가져오기 (없으면 0)
            eigen_main = centrality_data.get(main_keyword, 0)
            eigen_related = centrality_data.get(related_keyword, 0)

            # 키워드 조합을 항상 사전순으로 정렬하여 일관성 유지
            if main_keyword > related_keyword:
                main_keyword, related_keyword = related_keyword, main_keyword

            # 키워드 페어의 고유 식별자 생성
            pair = (main_keyword, related_keyword)

            if pair not in seen_pairs:
                # 역방향 유사도 확인 (related_keyword -> main_keyword)
                reverse_doc = collection_word2vec.find_one(
                    {"main_keyword": related_keyword, "related_keyword": main_keyword},
                    {"word2vec_minmax_score": 1}
                )
                reverse_w2v_score = reverse_doc["word2vec_minmax_score"] if reverse_doc else 0

                # 가중치를 적용한 우선순위 계산
                priority_score = (eigen_main * eigen_weight) + (eigen_related * eigen_weight) + (w2v_score * w2v_weight) + (reverse_w2v_score * w2v_weight)

                # 결과를 저장할 데이터 구조
                priority_result = {
                    'main_keyword': main_keyword,
                    'related_keyword': related_keyword,
                    'priority_score': priority_score
                }
                priority_results.append(priority_result)
                
                # 중복 방지 집합에 키워드 페어 추가
                seen_pairs.add(pair)

        # 우선순위 결과 MongoDB에 저장
        try:
            if priority_results:
                collection_priority.insert_many(priority_results)
                print("우선순위 계산 결과가 MongoDB의 priority_result 컬렉션에 저장되었습니다.")
        except Exception as e:
            print(f"우선순위 결과 저장 중 오류 발생: {e}")

        # 우선순위 정렬된 결과 반환
        sorted_priority_results = sorted(priority_results, key=lambda x: x['priority_score'], reverse=True)

        return sorted_priority_results

    except Exception as e:
        print(f"우선순위 계산 중 오류 발생: {e}")
        return []
