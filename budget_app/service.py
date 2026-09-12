import csv
from .models import Transaction
from .repository import BudgetRepository

class BudgetService:
    def __init__(self):
        self.repo = BudgetRepository()
        self.categories = ["식비", "교통", "쇼핑", "의료", "기타"]
        self.budget = 0

    def add_transaction(self, t_type, date, amount, category, memo, tags):
        tx_id = len(self.repo.get_all()) + 1
        new_tx = Transaction(tx_id, t_type, date, amount, category, memo, tags)
        self.repo.add(new_tx)
        return new_tx

    def get_transaction_list(self, limit=10):
        return self.repo.get_all()[-limit:]

    def get_monthly_summary(self, month_str):
        txs = [t for t in self.repo.get_all() if t.date.startswith(month_str)]
        summary = {
            "total_income": sum(t.amount for t in txs if t.type == "income"),
            "total_expense": sum(t.amount for t in txs if t.type == "expense"),
            "category_totals": {}
        }
        for t in txs:
            if t.type == "expense":
                summary["category_totals"][t.category] = summary["category_totals"].get(t.category, 0) + t.amount
        summary["balance"] = summary["total_income"] - summary["total_expense"]
        return summary

    def set_budget(self, amount):
        self.budget = amount

    def check_budget_status(self, month_str):
        expense = self.get_monthly_summary(month_str)["total_expense"]
        return self.budget - expense

    def export_to_csv(self, filename="export.csv"):
        txs = self.repo.get_all()
        if not txs: return False
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=txs[0].to_dict().keys())
            writer.writeheader()
            writer.writerows([t.to_dict() for t in txs])
        return True

    def search_transactions(self, keyword):
        return self.repo.search(keyword)

    def delete_transaction(self, tx_id):
        self.repo.delete(tx_id)

    def update_transaction(self, tx_id, **kwargs):
        return self.repo.update(tx_id, kwargs)