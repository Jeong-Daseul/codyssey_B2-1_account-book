from logic import add_transaction, get_transactions

def main():
    while True:
        print("\n--- 가계부 프로그램 ---")
        print("1. 거래 추가")
        print("2. 거래 목록 조회")
        print("q. 종료")
        choice = input("선택: ")

        if choice == '1':
            date = input("날짜 (YYYY-MM-DD): ")
            t_type = input("타입 (수입/지출): ")
            category = input("카테고리: ")
            amount = input("금액: ")
            memo = input("메모: ")
            
            new_id = add_transaction(date, t_type, category, amount, memo)
            print(f"✅ 저장 성공! (ID: {new_id})")

        elif choice == '2':
            limit_input = input("조회할 개수를 입력하세요 (전체는 엔터): ")
            limit = int(limit_input) if limit_input.isdigit() else None
            
            results = get_transactions(limit)
            
            print(f"\n--- 거래 목록 (최신순 {len(results)}건) ---")
            for item in results:
                print(f"[{item['id']}] {item['date']} | {item['type']} | {item['category']} | {item['amount']}원 | {item['memo']}")

        elif choice == 'q':
            break

if __name__ == "__main__":
    main()