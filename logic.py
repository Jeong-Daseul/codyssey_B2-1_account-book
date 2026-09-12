from storage import load_transactions, save_transactions, save_budget, load_budget

def add_transaction(date, t_type, category, amount, memo):
    """새로운 거래를 추가합니다."""
    transactions = load_transactions()
    
    # 새 거래 생성 (ID는 리스트 길이에 1을 더함)
    new_id = len(transactions) + 1
    new_item = {
        "id": new_id,
        "date": date,
        "type": t_type,
        "category": category,
        "amount": int(amount),
        "memo": memo
    }
    
    transactions.append(new_item)
    save_transactions(transactions)
    return new_id

def get_transactions(limit=None):
    """모든 거래 목록을 최신순으로 가져옵니다."""
    transactions = load_transactions()
    
    # 날짜 기준 최신순 정렬 (내림차순)
    sorted_list = sorted(transactions, key=lambda x: x['date'], reverse=True)
    
    if limit:
        return sorted_list[:limit]
    return sorted_list

def search_transactions(category=None, t_type=None, q=None):
    """조건에 맞는 거래를 검색합니다."""
    transactions = load_transactions()
    results = transactions
    
    if category:
        results = [item for item in results if item['category'] == category]
    if t_type:
        results = [item for item in results if item['type'] == t_type]
    if q:
        results = [item for item in results if q.lower() in item['memo'].lower()]
        
    return results

def get_monthly_summary(year, month):
    """특정 연도/월의 수입, 지출 요약을 계산합니다."""
    transactions = load_transactions()
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

def set_budget(amount):
    """예산을 설정합니다."""
    save_budget(amount)
    return f"새로운 예산 {amount:,}원이 설정되었습니다."

def get_budget_status():
    """현재 예산 대비 지출 현황을 계산합니다."""
    budget = load_budget()
    transactions = load_transactions()
    
    # 이번 달 지출 합계 계산 (지출만 합산)
    total_spending = sum(t['amount'] for t in transactions if t['type'] == '지출')
    
    remaining = budget - total_spending
    return {
        "budget": budget,
        "total_spending": total_spending,
        "remaining": remaining
    }

def get_category_stats():
    """카테고리별 지출 합계를 계산합니다."""
    transactions = load_transactions()
    stats = {}
    
    for t in transactions:
        if t['type'] == '지출':
            cat = t['category']
            amount = t['amount']
            # 카테고리가 이미 있으면 더하고, 없으면 새로 생성
            stats[cat] = stats.get(cat, 0) + amount
            
    # 금액이 높은 순서대로 정렬
    sorted_stats = dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))
    return sorted_stats