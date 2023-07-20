from typing import List
from exceptions import InvalidBill
from models.account import User
from models.bill import Bill, EqualBill, ExactBill, PercentBill
from models.split import PayerSplit, Split, SplitType


class BillFactory:
    def create_bill(
        self,
        split_type: SplitType,
        title: str,
        amount: float,
        participants: List[User],
        splits: List[Split],
        payers: List[PayerSplit],
    ) -> Bill:
        match split_type:
            case SplitType.EXACT:
                bill = ExactBill(title, amount, splits)
            case SplitType.EQUAL:
                bill = EqualBill(title, amount, participants)
            case SplitType.PERCENT:
                bill = PercentBill(title, amount, splits)
        bill.set_payers(payers)
        for split in bill.splits:
            print(split.amount)
        if not bill.are_valid_splits():
            raise InvalidBill("invalid bill splits")

        return bill
