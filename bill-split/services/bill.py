from typing import List
from exceptions import DoesNotExists, InvalidBill
from models.account import User

from models.bill import Bill, EqualBill, ExactBill, PercentBill
from models.split import ExactSplit, PayerSplit, Split, SplitType
from services.factory import BillFactory


class BillService:
    def __init__(self, bill_repo, user_repo, group_repo, balance_repo) -> None:
        self.bill_repo = bill_repo
        self.group_repo = group_repo
        self.user_repo = user_repo
        self.balance_repo = balance_repo

    def create_bill(
        self,
        split_type: SplitType,
        title: str,
        amount: float,
        payers: List[PayerSplit],
        splits: List[Split],
    ) -> Bill:
        # validate users
        for split in payers:
            if not self.user_repo.get(split.user_id):
                raise DoesNotExists("payer with given id does not exists")

        # validate split users
        participants = []
        for split in splits:
            user = self.user_repo.get(split.user_id)
            if not user:
                raise DoesNotExists("user with given id does not exists")
            participants.append(user)

        bill = BillFactory().create_bill(
            split_type, title, amount, participants, splits, payers
        )
        self.bill_repo.add(bill)

        self.update_balances(bill)
        return bill

    def create_group_bill(
        self,
        group_id: str,
        split_type: SplitType,
        title: str,
        amount: float,
        payers: List[PayerSplit],
        splits: List[Split],
    ) -> Bill:
        group = self.group_repo.get(group_id)
        bill = self.create_bill(split_type, title, amount, payers, splits)
        group.add_bill(bill)
        return bill

    def update_balances(self, bill):
        shares = {}
        for split in bill.payers:
            shares[split.user_id] = split.amount

        for split in bill.splits:
            if not shares.get(split.user_id):
                shares[split.user_id] = 0
            shares[split.user_id] -= split.amount

        positives = [
            {"user": user_id, "amount": shares[user_id]}
            for user_id in shares
            if shares[user_id] > 0
        ]
        negatives = [
            {"user": user_id, "amount": shares[user_id]}
            for user_id in shares
            if shares[user_id] < 0
        ]
        # print("shares", shares)

        for i in range(len(positives)):
            for j in range(len(negatives)):
                amount = min(positives[i]["amount"], -negatives[j]["amount"])
                positives[i]["amount"] -= amount
                negatives[j]["amount"] += amount
                # print("amount", amount, "pos", positives[i], "neg", negatives[j])
                self.balance_repo.set_balance(
                    positives[i]["user"], negatives[j]["user"], round(amount, 2)
                )
                self.balance_repo.set_balance(
                    negatives[j]["user"], positives[i]["user"], round(-amount, 2)
                )
                # print("balances", self.balance_repo.balances)
                if positives[i]["amount"] == 0:
                    i += 1
                if negatives[j]["amount"] == 0:
                    j += 1
