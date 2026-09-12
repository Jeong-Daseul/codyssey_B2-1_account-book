import json
import os
from .models import Transaction

class BudgetRepository:
    def __init__(self, filename="data.jsonl"):
        self.filename = filename

    def save_all(self, transactions):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for tx in transactions:
                f.write(json.dumps(tx.to_dict(), ensure_ascii=False) + "\n")

    def get_all(self):
        if not os.path.exists(self.filename):
            return []
        transactions = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                transactions.append(Transaction(**data))
        return transactions

    def add(self, transaction):
        txs = self.get_all()
        txs.append(transaction)
        self.save_all(txs)

    def update(self, tid, amount, memo, category):
        txs = self.get_all()
        found = False
        for t in txs:
            if t.id == tid:
                t.amount = amount
                t.memo = memo
                t.category = category
                found = True
                break
        if found:
            self.save_all(txs)
        return found

    def delete(self, tid):
        txs = self.get_all()
        new_txs = [t for t in txs if t.id != tid]
        if len(txs) != len(new_txs):
            self.save_all(new_txs)
            return True
        return False