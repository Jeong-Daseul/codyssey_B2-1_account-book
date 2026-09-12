import csv
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

def delete_transaction(t_id):
    """ID를 기반으로 거래 내역을 삭제합니다."""
    transactions = load_transactions()
    
    # 입력받은 ID와 일치하지 않는 것들만 남깁니다 (필터링)
    new_transactions = [t for t in transactions if t['id'] != t_id]
    
    if len(new_transactions) == len(transactions):
        return False, f"❌ ID {t_id}를 찾을 수 없습니다."
    
    save_transactions(new_transactions)
    return True, f"✅ ID {t_id} 내역이 성공적으로 삭제되었습니다."


def update_transaction(t_id, date=None, t_type=None, category=None, amount=None, memo=None):
    """
    특정 ID의 거래 내역을 수정합니다. 
    값이 전달된 항목만 수정하고, None인 항목은 기존 값을 유지합니다.
    """
    transactions = load_transactions()
    is_found = False
    
    for t in transactions:
        if t['id'] == t_id:
            if date: t['date'] = date
            if t_type: t['type'] = t_type
            if category: t['category'] = category
            if amount is not None: t['amount'] = amount
            if memo is not None: t['memo'] = memo
            is_found = True
            break
    
    if is_found:
        save_transactions(transactions)
        return True, f"✅ [ID: {t_id}] 내역이 성공적으로 수정되었습니다."
    else:
        return False, f"❌ [ID: {t_id}] 내역을 찾을 수 없습니다."


def export_to_csv(filename="account_book.csv"):
    transactions = load_transactions()
    if not transactions:
        return False, "내보낼 데이터가 없습니다."
    
    try:
        # utf-8-sig는 엑셀에서 한글이 깨지지 않게 해주는 인코딩 방식입니다.
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            # 데이터의 키(id, date, type...)를 헤더로 사용합니다.
            fieldnames = transactions[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader() # 첫 줄에 제목 쓰기
            writer.writerows(transactions) # 데이터 쓰기
            
        return True, f"✅ {filename} 파일로 저장되었습니다!"
    except Exception as e:
        return False, f"❌ 오류 발생: {str(e)}"