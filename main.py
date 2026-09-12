# logic.py에서 필요한 함수들을 모두 가져옵니다.
from logic import (
    add_transaction, get_transactions, search_transactions, 
    get_monthly_summary, set_budget, get_budget_status,
    get_category_stats,
    delete_transaction,
    update_transaction  # 추가
)

def main():
    while True:
        print("\n--- 파이썬 가계부 ---")
        print("1. 거래 추가")
        print("2. 거래 목록 조회")
        print("3. 거래 검색")
        print("4. 월별 요약")
        print("5. 예산 설정/현황")
        print("6. 카테고리별 통계")
        print("7. 거래 삭제")
        print("8. 거래 수정")  # 추가
        print("0. 종료")
        choice = input("선택: ")

        if choice == '1':
            date = input("날짜 (YYYY-MM-DD): ")
            t_type = input("타입 (수입/지출): ")
            category = input("카테고리: ")
            amount = int(input("금액: "))
            memo = input("메모: ")
            new_id = add_transaction(date, t_type, category, amount, memo)
            print(f"✅ 저장 성공! (ID: {new_id})")

        elif choice == '2':
            limit_input = input("조회할 개수를 입력하세요 (전체는 엔터): ")
            limit = int(limit_input) if limit_input.isdigit() else None
            results = get_transactions(limit)
            print(f"\n--- 거래 목록 (최신순 {len(results)}건) ---")
            for item in results:
                print(f"[{item['id']}] {item['date']} | {item['type']} | {item['category']} | {item['amount']:,}원 | {item['memo']}")

        elif choice == '3':
            print("\n--- 거래 검색 ---")
            category = input("카테고리 (건너뛰려면 엔터): ") or None
            t_type = input("타입 (수입/지출, 건너뛰려면 엔터): ") or None
            q = input("메모 검색어 (건너뛰려면 엔터): ") or None
            results = search_transactions(category=category, t_type=t_type, q=q)
            print(f"\n🔍 검색 결과 ({len(results)}건)")
            for item in results:
                print(f"[{item['id']}] {item['date']} | {item['type']} | {item['category']} | {item['amount']:,}원 | {item['memo']}")

        elif choice == '4':
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
            status = get_budget_status() 
            print(f"현재 설정된 예산: {status['budget']:,}원")
            print(f"현재까지 총 지출: {status['total_spending']:,}원")
            print(f"남은 예산: {status['remaining']:,}원")
            print("---------------------------")
            # 예산 설정 질문은 5번 메뉴 안에 있어야 합니다!
            new_budget = input("새로운 예산을 설정하시겠습니까? (금액 입력 / 취소는 Enter): ")
            if new_budget.isdigit():
                msg = set_budget(int(new_budget))
                print(msg)

        elif choice == '6':
            stats = get_category_stats()
            print("\n--- 카테고리별 지출 통계 ---")
            if not stats:
                print("지출 내역이 없습니다.")
            else:
                for cat, total in stats.items():
                    print(f"[{cat}] {total:,}원")


        elif choice == '7':
            print("\n--- 거래 내역 삭제 ---")

            # 1. 최근 내역 5개를 먼저 보여줌 (ID 확인용)
            recent_list = get_transactions(limit=5)
            if not recent_list:
                print("삭제할 내역이 없습니다.")
                continue
            
            print("최근 내역 (최대 5건):")

            for t in recent_list:
                print(f"[{t['id']}] {t['date']} | {t['category']} | {t['amount']:,}원 | {t['memo']}")

            
            try:
                # 2. 보여준 목록을 보고 ID 입력받기
                target_id = int(input("\n삭제할 거래의 ID를 입력하세요 (취소: 0): "))
                if target_id == 0:
                    print("삭제가 취소되었습니다.")
                    continue
                    
                success, message = delete_transaction(target_id)
                print(message)
            except ValueError:
                print("⚠️ 숫자로 된 ID를 입력해 주세요.")

        elif choice == '8':
            print("\n--- 거래 내역 수정 ---")
            recent_list = get_transactions(limit=5)
            if not recent_list:
                print("수정할 내역이 없습니다.")
                continue
            
            print("최근 내역 (최대 5건):")
            for t in recent_list:
                print(f"[{t['id']}] {t['date']} | {t['type']} | {t['category']} | {t['amount']:,}원 | {t['memo']}")
            
            try:
                target_id = int(input("\n수정할 거래의 ID를 입력하세요: "))
                
                print("\n새로운 정보를 입력하세요 (변경하지 않으려면 엔터)")
                new_date = input("새 날짜 (YYYY-MM-DD): ") or None
                new_type = input("새 타입 (수입/지출): ") or None
                new_cat = input("새 카테고리: ") or None
                new_amt_input = input("새 금액: ")
                new_amt = int(new_amt_input) if new_amt_input else None
                new_memo = input("새 메모: ") or None
                
                success, message = update_transaction(
                    target_id, date=new_date, t_type=new_type, 
                    category=new_cat, amount=new_amt, memo=new_memo
                )
                print(message)
                
            except ValueError:
                print("⚠️ 올바른 숫자를 입력해 주세요.")



        elif choice == '0': # 메뉴판에 맞춰 '0'으로 수정했습니다.
            print("프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break

if __name__ == "__main__":
    main()