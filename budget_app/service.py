import csv
from .models import Transaction
from .repository import BudgetRepository

class BudgetService:
    def __init__(self):
        self.repo = BudgetRepository()
        self.income_categories = ["급여", "용돈", "이자", "기타수입"]
        self.expense_categories = ["식비", "교통", "쇼핑", "의료", "기타지출"]
        self.budgets = {}

    def generate_id(self, date_str):
        """YYYYMMDDNNN 형식의 ID 생성"""
        clean_date = date_str.replace("-", "")
        existing_txs = [t for t in self.repo.get_all() if t.date == date_str]
        seq = len(existing_txs) + 1
        return int(f"{clean_date}{seq:03d}")

    def get_categories(self, t_type):
        return self.income_categories if t_type == "수입" else self.expense_categories

    def add_transaction(self, t_type, date, amount, category, memo, tags):
        tid = self.generate_id(date)
        new_tx = Transaction(tid, t_type, date, amount, category, memo, tags)
        self.repo.add(new_tx)

    def get_transaction_list(self):
        return self.repo.get_all()

    def get_monthly_summary(self, month):
        txs = self.repo.get_all()
        summary = {"수입": 0, "지출": 0, "카테고리별": {}}
        for t in txs:
            if t.date.startswith(month):
                summary[t.type] += t.amount
                if t.type == "지출":
                    summary["카테고리별"][t.category] = summary["카테고리별"].get(t.category, 0) + t.amount
        return summary

    def search_transactions(self, keyword):
        return [t for t in self.repo.get_all() if keyword in t.memo or keyword in t.category]

    def update_transaction(self, tid, amount, memo, category):
        return self.repo.update(tid, amount, memo, category)

    def delete_transaction(self, tid):
        return self.repo.delete(tid)

    def export_to_csv(self, filename="export.csv"):
        txs = self.repo.get_all()
        if not txs: return False
        # utf-8-sig는 엑셀에서 한글 깨짐을 방지합니다.
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "구분", "날짜", "금액", "카테고리", "메모", "태그"])
            for t in txs:
                tag_str = ", ".join(t.tags) if isinstance(t.tags, list) else t.tags
                writer.writerow([t.id, t.type, t.date, t.amount, t.category, t.memo, tag_str])
        return True

    def visualize_expenses(self):
        txs = self.repo.get_all()
        stats = {}
        for t in txs:
            if t.type == '지출':
                stats[t.category] = stats.get(t.category, 0) + t.amount
        if not stats:
            print("데이터가 없습니다.")
            return
        print("\n[지출 시각화]")
        for cat, amt in stats.items():
            bar = "■" * (amt // 5000)
            print(f"{cat:<5}: {bar} ({amt:,}원)")