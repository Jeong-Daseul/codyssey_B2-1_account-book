import json
import os
from models import Transaction

DATA_FILE = "data.json"

# 데이터를 파일에 저장하는 함수
def save_data(transactions: list[Transaction]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(transactions, f, ensure_ascii=False, indent=4)

# 파일에서 데이터를 불러오는 함수 (제너레이터 사용)
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            yield item  # 데이터를 하나씩 꺼내주는 제너레이터 방식!

# 제너레이터로 가져온 데이터를 리스트로 변환
def get_all_transactions() -> list[Transaction]:
    return list(load_data())