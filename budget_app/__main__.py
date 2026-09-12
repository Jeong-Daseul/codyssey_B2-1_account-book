import sys
from .service import BudgetService
from .utils import handle_errors, log_action

class BudgetApp:
    def __init__(self):
        self.service = BudgetService()

    def display_menu(self):
        print("\n" + "="*40)
        print("   💰 실무형 가계부 관리 시스템 (Full v1.0)")
        print("="*40)
        print("1. 내역 추가")
        print("2. 최근 내역 보기")
        print("3. 월별 요약 통계")
        print("4. 내역 검색")
        print("5. 예산 설정/확인")
        print("6. 카테고리 관리")
        print("7. 내역 수정")
        print("8. 내역 삭제")
        print("9. CSV 내보내기")
        print("10. 종료")
        print("="*40)

    @handle_errors
    @log_action
    def run_add(self):
        print("\n[내역 추가]")
        t_type = input("구분(income/expense): ")
        date = input("날짜(YYYY-MM-DD): ")
        amount = int(input("금액: "))
        category = input(f"카테고리({', '.join(self.service.categories)}): ")
        memo = input("메모: ")
        self.service.add_transaction(t_type, date, amount, category, memo, [])
        print("✅ 추가되었습니다.")

    @handle_errors
    def run_list(self):
        txs = self.service.get_transaction_list()
        for t in txs:
            print(f"{t.id} | {t.date} | {t.type} | {t.amount:,}원 | {t.category} | {t.memo}")

    @handle_errors
    def run_search(self):
        kw = input("검색어 입력: ")
        results = self.service.search_transactions(kw)
        for t in results:
            print(f"{t.id} | {t.date} | {t.amount:,}원 | {t.memo}")

    @handle_errors
    def run_export(self):
        if self.service.export_to_csv():
            print("✅ export.csv 파일로 저장되었습니다.")

    def main(self):
        while True:
            self.display_menu()
            choice = input("선택: ").strip()
            if choice == '1': self.run_add()
            elif choice == '2': self.run_list()
            elif choice == '3':
                m = input("조회 월(YYYY-MM): ")
                s = self.service.get_monthly_summary(m)
                print(f"지출 합계: {s['total_expense']:,}원")
            elif choice == '4': self.run_search()
            elif choice == '9': self.run_export()
            elif choice == '10': break
            else: print("준비 중이거나 잘못된 입력입니다.")

if __name__ == "__main__":
    app = BudgetApp()
    app.main()