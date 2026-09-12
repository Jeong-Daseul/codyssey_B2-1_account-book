import sys
from .service import BudgetService
from .utils import handle_errors, log_action

class BudgetApp:
    def __init__(self):
        self.service = BudgetService()

    def display_menu(self):
        print("\n" + "═"*45)
        print("   💰 실무형 가계부 관리 시스템 (Full v1.0)")
        print("═"*45)
        print(" 1. 내역 추가")
        print(" 2. 전체 내역 보기")
        print(" 3. 월별 요약 통계")
        print(" 4. 내역 검색")
        print(" 5. 예산 설정/확인")
        print(" 6. 카테고리 관리")
        print(" 7. 내역 수정")
        print(" 8. 내역 삭제")
        print(" 9. CSV 내보내기")
        print(" 10. 지출 시각화(차트)")
        print(" 0. 종료")
        print("═"*45)

    @handle_errors
    @log_action
    def run_add(self):
        print("\n[1. 내역 추가]")
        t_type = input("구분 (수입/지출): ").strip()
        cats = self.service.get_categories(t_type)
        date = input("날짜 (YYYY-MM-DD): ").strip()
        amount = int(input("금액: ").strip())
        print(f"추천 카테고리: {', '.join(cats)}")
        category = input("카테고리 선택: ").strip()
        memo = input("메모: ").strip()
        self.service.add_transaction(t_type, date, amount, category, memo, [])
        print("✅ 추가 완료!")

    @handle_errors
    def run_list(self):
        print("\n[2. 전체 내역]")
        txs = self.service.get_transaction_list()
        if not txs:
            print("데이터가 없습니다.")
            return
        for t in txs:
            print(f"ID:{t.id} | {t.date} | {t.type} | {t.amount:,}원 | {t.category} | {t.memo}")

    @handle_errors
    def run_summary(self):
        print("\n[3. 월별 요약]")
        month = input("조회 월(YYYY-MM): ").strip()
        s = self.service.get_monthly_summary(month)
        print(f"\n📊 {month} 요약 결과")
        print(f"💰 총 수입: {s['수입']:,}원")
        print(f"💸 총 지출: {s['지출']:,}원")
        print(f"⚖️ 잔액: {s['수입'] - s['지출']:,}원")
        print("-" * 20)
        print("[카테고리별 지출 상세]")
        for cat, amt in s['카테고리별'].items():
            print(f"- {cat}: {amt:,}원")

    @handle_errors
    def run_search(self):
        print("\n[4. 검색]")
        keyword = input("검색어 입력: ").strip()
        results = self.service.search_transactions(keyword)
        for t in results:
            print(f"ID:{t.id} | {t.date} | {t.type} | {t.amount:,}원 | {t.category} | {t.memo}")

    @handle_errors
    def run_budget(self):
        print("\n[5. 예산 설정/확인]")
        if self.service.budgets:
            print("현재 예산 현황:")
            for cat, amt in self.service.budgets.items():
                print(f"- {cat}: {amt:,}원")
        else:
            print("설정된 예산이 없습니다.")
        
        ans = input("\n예산을 설정하시겠습니까? (y/n): ").lower()
        if ans == 'y':
            cat = input("카테고리: ").strip()
            amt = int(input("예산 금액: ").strip())
            self.service.budgets[cat] = amt
            print(f"✅ {cat} 예산 설정 완료!")

    @handle_errors
    def run_categories(self):
        while True:
            print("\n[6. 카테고리 관리]")
            print(f"💰 수입: {', '.join(self.service.income_categories)}")
            print(f"💸 지출: {', '.join(self.service.expense_categories)}")
            print("-" * 20)
            print("1. 추가 | 2. 삭제 | 0. 돌아가기")
            sub_choice = input("선택: ").strip()
            if sub_choice == '1':
                t_type = input("구분(수입/지출): ").strip()
                new_cat = input("추가할 카테고리명: ").strip()
                if t_type == "수입": self.service.income_categories.append(new_cat)
                else: self.service.expense_categories.append(new_cat)
            elif sub_choice == '2':
                t_type = input("구분(수입/지출): ").strip()
                del_cat = input("삭제할 카테고리명: ").strip()
                target = self.service.income_categories if t_type == "수입" else self.service.expense_categories
                if del_cat in target: target.remove(del_cat)
            elif sub_choice == '0': break

    @handle_errors
    def run_update(self):
        print("\n[7. 내역 수정]")
        txs = self.service.get_transaction_list()
        if not txs:
            print("수정할 데이터가 없습니다.")
            return

        self.run_list()
        tid = int(input("\n수정할 내역 ID를 입력하세요: ").strip())
        
        target_tx = next((t for t in txs if t.id == tid), None)
        if not target_tx:
            print("❌ 해당 ID를 찾을 수 없습니다.")
            return

        print(f"\n현재 정보: [{target_tx.type}] {target_tx.category} | {target_tx.amount:,}원 | {target_tx.memo}")
        
        amount = int(input("새 금액: ").strip())
        memo = input("새 메모: ").strip()
        
        cats = self.service.get_categories(target_tx.type)
        print(f"사용 가능 카테고리: {', '.join(cats)}")
        category = input("새 카테고리 선택: ").strip()
        
        if self.service.update_transaction(tid, amount, memo, category):
            print("✅ 수정 성공!")
        else: 
            print("❌ 수정 실패.")

    @handle_errors
    def run_delete(self):
        print("\n[8. 내역 삭제]")
        txs = self.service.get_transaction_list()
        if not txs:
            print("삭제할 데이터가 없습니다.")
            return
            
        self.run_list()
        tid = int(input("\n삭제할 내역 ID를 입력하세요: ").strip())
        if self.service.delete_transaction(tid):
            print("✅ 삭제 성공!")
        else: print("❌ ID를 확인해주세요.")

    def main(self):
        while True:
            self.display_menu()
            choice = input("선택: ").strip()
            if choice == '1': self.run_add()
            elif choice == '2': self.run_list()
            elif choice == '3': self.run_summary()
            elif choice == '4': self.run_search()
            elif choice == '5': self.run_budget()
            elif choice == '6': self.run_categories()
            elif choice == '7': self.run_update()
            elif choice == '8': self.run_delete()
            elif choice == '9':
                if self.service.export_to_csv():
                    print("✅ export.csv 파일로 저장되었습니다.")
                else:
                    print("❌ 내보낼 데이터가 없습니다.")
            elif choice == '10':
                self.service.visualize_expenses()
            elif choice == '0':
                print("종료합니다. 수고하셨습니다!")
                break

if __name__ == "__main__":
    app = BudgetApp()
    app.main()