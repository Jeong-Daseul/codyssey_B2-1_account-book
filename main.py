# logic.py에서 필요한 함수들을 모두 가져옵니다.
# set_budget과 get_budget_status를 추가로 가져와야 합니다!
from logic import add_transaction, get_transactions, search_transactions, get_monthly_summary, set_budget, get_budget_status

def main():
    while True:
        print("\n--- 가계부 프로그램 ---")
        print("1. 거래 추가")
        print("2. 거래 목록 조회")
        print("3. 거래 검색")
        print("4. 월별 요약")
        print("5. 예산 설정 및 현황") # <--- 이 줄을 추가해야 메뉴에 보입니다!
        print("q. 종료")
        choice = input("선택: ")

        if choice == '1':
            # ... (기존 코드와 동일)
            date = input("날짜 (YYYY-MM-DD): ")
            t_type = input("타입 (수입/지출): ")
            category = input("카테고리: ")
            amount = int(input("금액: "))
            memo = input("메모: ")
            new_id = add_transaction(date, t_type, category, amount, memo)
            print(f"✅ 저장 성공! (ID: {new_id})")

        elif choice == '2':
            # ... (기존 코드와 동일)
            limit_input = input("조회할 개수를 입력하세요 (전체는 엔터): ")
            limit = int(limit_input) if limit_input.isdigit() else None
            results = get_transactions(limit)
            print(f"\n--- 거래 목록 (최신순 {len(results)}건) ---")
            for item in results:
                print(f"[{item['id']}] {item['date']} | {item['type']} | {item['category']} | {item['amount']:,}원 | {item['memo']}")

        elif choice == '3':
            # ... (기존 코드와 동일)
            print("\n--- 거래 검색 ---")
            category = input("카테고리 (건너뛰려면 엔터): ") or None
            t_type = input("타입 (수입/지출, 건너뛰려면 엔터): ") or None
            q = input("메모 검색어 (건너뛰려면 엔터): ") or None
            results = search_transactions(category=category, t_type=t_type, q=q)
            print(f"\n🔍 검색 결과 ({len(results)}건)")
            for item in results:
                print(f"[{item['id']}] {item['date']} | {item['type']} | {item['category']} | {item['amount']:,}원 | {item['memo']}")

        elif choice == '4':
            # ... (기존 코드와 동일)
            print("\n--- 월별 요약 ---")
            year = input("연도 (YYYY): ")
            month = input("월 (MM): ")
            summary = get_monthly_summary(year, month)
            print(f"\n📊 {year}년 {month}월 요약 결과")
            print(f"💰 총 수입: {summary['income']:,}원")
            print(f"💸 총 지출: {summary['expense']:,}원")
            print(f"⚖️ 잔액: {summary['balance']:,}원")

        elif choice == '5':
            print("\n--- [예산 설정 및 현황] ---")
            # logic.get_budget_status() 대신 바로 get_budget_status() 호출
            status = get_budget_status() 
            print(f"현재 설정된 예산: {status['budget']:,}원")
            print(f"현재까지 총 지출: {status['total_spending']:,}원")
            print(f"남은 예산: {status['remaining']:,}원")
            print("---------------------------")
            
            new_budget = input("새로운 예산을 설정하시겠습니까? (금액 입력 / 취소는 Enter): ")
            if new_budget.isdigit():
                # logic.set_budget() 대신 바로 set_budget() 호출
                msg = set_budget(int(new_budget))
                print(msg)

        elif choice == 'q':
            print("프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break

if __name__ == "__main__":
    main()