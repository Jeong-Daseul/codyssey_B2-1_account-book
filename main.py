from logic import add_transaction, get_summary, search_by_category

def main():
    while True:
        print("\n--- 💰 심플 가계부 프로그램 ---")
        print("1. 내역 추가")
        print("2. 전체 요약 보기")
        print("3. 카테고리 검색")
        print("4. 종료")
        
        choice = input("원하는 메뉴 번호를 선택하세요: ")

        if choice == '1':
            date = input("날짜 (YYYY-MM-DD): ")
            type_input = input("종류 (수입/지출): ")
            # 프로그램 내부 처리를 위해 영문으로 변환
            t_type = "income" if type_input == "수입" else "expense"
            category = input("카테고리 (예: 식비, 월급): ")
            amount = int(input("금액: "))
            memo = input("메모: ")
            
            add_transaction(date, t_type, category, amount, memo)

        elif choice == '2':
            income, expense, balance = get_summary()
            print(f"\n[ 요약 결과 ]")
            print(f"💵 총 수입: {income}원")
            print(f"💸 총 지출: {expense}원")
            print(f"⚖️ 잔액: {balance}원")

        elif choice == '3':
            cat = input("검색할 카테고리를 입력하세요: ")
            results = search_by_category(cat)
            print(f"\n[ '{cat}' 검색 결과 ]")
            for r in results:
                t_symbol = "➕" if r['type'] == 'income' else "➖"
                print(f"- {r['date']} | {t_symbol} {r['amount']}원 ({r['memo']})")

        elif choice == '4':
            print("프로그램을 종료합니다. 오늘도 알뜰한 하루 되세요!")
            break
        else:
            print("❌ 잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    main()
    