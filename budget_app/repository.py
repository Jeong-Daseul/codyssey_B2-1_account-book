import json
import os
from .models import Transaction

class BudgetRepository:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.transactions = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Transaction(**item) for item in data]

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.transactions], f, ensure_ascii=False, indent=4)

    def add(self, transaction):
        self.transactions.append(transaction)
        self.save()

    def get_all(self):
        return self.transactions

    def find_by_id(self, tx_id):
        return next((t for t in self.transactions if t.id == tx_id), None)

    def delete(self, tx_id):
        self.transactions = [t for t in self.transactions if t.id != tx_id]
        self.save()

    def search(self, keyword):
        return [t for t in self.transactions if keyword in t.memo or keyword in t.category]

    def update(self, tx_id, updated_data):
        tx = self.find_by_id(tx_id)
        if tx:
            for key, value in updated_data.items():
                setattr(tx, key, value)
            self.save()
            return True
        return False