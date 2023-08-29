from flask import Flask, request, jsonify
import pickle
import pymysql
import pandas as pd
import random
import json

app = Flask(__name__)

# 저장한 모델 파일 불러오기
# filename = 'word2vec_model.pkl'
filename = 'new_word2vec_model.pkl'
with open(filename, 'rb') as file:
    loaded_model = pickle.load(file)

# MySQL 서버 연결 정보

db_config = {
    'host': "playdata.cqro5qdbxzm7.ap-northeast-2.rds.amazonaws.com",
    'port': 3306,
    'user': 'admin',
    'passwd': 'qwer1234!',
    'db': 'summermart',
    'charset': 'utf8'
}
# db_config = {
#     'host': "",
#     'port': 3306,
#     'user': '',
#     'passwd': '',
#     'db': '',
#     'charset': 'utf8'
# }

# Function to find similar product names
def find_similar_products(input_word):

    # Connect to MySQL database
    connection = pymysql.connect(**db_config)

    # 단어가 어휘에 없으면 빈 리스트 반환
    if input_word not in loaded_model.wv:
        return []  
    
    # Find similar words using the loaded model
    similar_words = loaded_model.wv.most_similar(input_word, topn=5)
    
    similar_product_names = []
    
    for word, score in similar_words:

        # id, name 출력
        # Search the database for product names with similar words
        query = f"SELECT id, name FROM product WHERE name LIKE '%{word}%'"
        similar_products_df = pd.read_sql(query, connection)
        similar_product_names.extend(similar_products_df.to_dict(orient='records'))
    
    # Randomly limit results to 5
    random.shuffle(similar_product_names)
    limited_results = similar_product_names[:5]
    
    return limited_results

# JSON으로 입출력
@app.route('/get_similar_products', methods=['POST'])
def get_similar_products():

    data = request.get_json()  # Get JSON data from request    
    result = find_similar_products(data["input_word"])    
    result = json.dumps (result, ensure_ascii=False)
    return result # Return JSON response

if __name__ == '__main__':
    app.run(host='0.0.0.0')