from storage import save_data, load_data
from datetime import datetime

TRANSACTIONS_FILE = 'transactions.json'

def add_transaction(date, type, category, amount, memo):
    transactions = load_data(TRANSACTIONS_FILE)
    
    # 새 거래 생성 (ID는 리스트 길이에 1을 더함)
    new_id = len(transactions) + 1
    new_item = {
        "id": new_id,
        "date": date,
        "type": type,
        "category": category,
        "amount": int(amount),
        "memo": memo
    }
    
    transactions.append(new_item)
    save_data(TRANSACTIONS_FILE, transactions)
    return new_id

def get_transactions(limit=None):
    transactions = load_data(TRANSACTIONS_FILE)
    
    # 날짜 기준 최신순 정렬 (내림차순)
    # 날짜 문자열(YYYY-MM-DD)을 비교하여 정렬합니다.
    sorted_list = sorted(transactions, key=lambda x: x['date'], reverse=True)
    
    # limit이 있으면 그 개수만큼만 자르기
    if limit:
        return sorted_list[:limit]
    return sorted_list

# logic.py에 추가

def get_monthly_summary(year, month):
    transactions = load_data(TRANSACTIONS_FILE)
    total_income = 0
    total_expense = 0
    
    # 입력받은 월을 "01", "02" 형태로 맞춥니다.
    target_month = f"{year}-{month.zfill(2)}" 
    
    for item in transactions:
        # 날짜(YYYY-MM-DD)가 "YYYY-MM"으로 시작하는지 확인
        if item['date'].startswith(target_month):
            if item['type'] == '수입':
                total_income += item['amount']
            elif item['type'] == '지출':
                total_expense += item['amount']
                
    return {
        "income": total_income,
        "expense": total_expense,
        "balance": total_income - total_expense
    }

def search_transactions(category=None, t_type=None, q=None):
    transactions = load_data(TRANSACTIONS_FILE)
    results = transactions
    
    # 카테고리 필터
    if category:
        results = [item for item in results if item['category'] == category]
    
    # 타입 필터 (수입/지출)
    if t_type:
        results = [item for item in results if item['type'] == t_type]
        
    # 메모 검색어 필터
    if q:
        results = [item for item in results if q.lower() in item['memo'].lower()]
        
    return results

def get_monthly_summary(year, month):
    transactions = load_data(TRANSACTIONS_FILE)
    total_income = 0
    total_expense = 0
    
    # 월 형식을 "YYYY-MM"으로 맞춤 (예: 2023-05)
    target_month = f"{year}-{month.zfill(2)}" 
    
    for item in transactions:
        if item['date'].startswith(target_month):
            if item['type'] == '수입':
                total_income += item['amount']
            elif item['type'] == '지출':
                total_expense += item['amount']
                
    return {
        "income": total_income,
        "expense": total_expense,
        "balance": total_income - total_expense
    }