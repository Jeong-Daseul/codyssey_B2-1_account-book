import json
import os

# 데이터 파일 경로 설정
DATA_FILE = 'transactions.json'
BUDGET_FILE = 'budget.json'

def load_transactions():
    """파일에서 거래 내역을 불러옵니다."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_transactions(transactions):
    """거래 내역을 파일에 저장합니다."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=4, ensure_ascii=False)

def load_budget():
    """파일에서 설정된 예산을 불러옵니다."""
    if not os.path.exists(BUDGET_FILE):
        return 0  # 설정된 예산이 없으면 0원 반환
    with open(BUDGET_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("budget", 0)

def save_budget(amount):
    """예산을 파일에 저장합니다."""
    with open(BUDGET_FILE, 'w', encoding='utf-8') as f:
        json.dump({"budget": amount}, f, indent=4, ensure_ascii=False)