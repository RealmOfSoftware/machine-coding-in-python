from typing import List
from exceptions import InvalidBill
from models.account import User

from models.split import EqualSplit, ExactSplit, PayerSplit, Split, SplitType


class Bill:
    def __init__(self, title: str, amount: float):
        self.id = None
        self.title = title
        self.amount = amount
        self.payers = []
        self.splits = []
        self.split_type: SplitType = None

    def set_payers(self, payers: List[PayerSplit]):
        self.payers = payers
        if not self.are_valid_payers():
            raise InvalidBill("invalid payers")

    def are_valid_splits(self) -> bool:
        amount = sum([split.amount for split in self.splits])
        return abs(amount - self.amount) < 1

    def are_valid_payers(self) -> bool:
        amount = sum([split.amount for split in self.payers])
        return amount == self.amount


class EqualBill(Bill):
    def __init__(self, title: str, amount: float, participants: List[User]) -> None:
        super().__init__(title, amount)

        split_amount = round(amount / len(participants), 2)
        splits = []
        for participant in participants:
            split = EqualSplit(participant.id)
            split.set_amount(split_amount)
            splits.append(split)
        self.splits = splits
        self.split_type = SplitType.EQUAL

    def are_valid_splits(self) -> bool:
        if len(self.splits) == 0:
            return self.amount == 0

        if not super().are_valid_splits():
            return False

        last_amount = self.splits[0].amount
        for i in range(1, len(self.splits)):
            if abs(self.splits[i].amount - last_amount) > 1:
                return False

        return True

    def add_participant(self, user) -> None:
        pass

    def remove_participant(self, user) -> None:
        pass


class ExactBill(Bill):
    def __init__(self, title: str, amount: float, splits: List[ExactSplit]) -> None:
        super().__init__(title, amount)

        self.splits = splits
        self.split_type = SplitType.EXACT


class PercentBill(Bill):
    def __init__(self, title, amount, splits: List[Split]) -> None:
        super().__init__(title, amount)

        for split in splits:
            split.amount = round(amount * split.percent / 100, 2)
        self.splits = splits
        self.split_type = SplitType.PERCENT

    def are_valid_splits(self):
        if not super().are_valid_splits():
            return False

        total_percent = sum([split.percent for split in self.splits])
        return total_percent == 100
