from enum import Enum


class SplitType(str, Enum):
    EXACT = "EXACT"
    PERCENT = "PERCENT"
    EQUAL = "EQUAL"


class Split:
    def __init__(self, user_id) -> None:
        self.user_id: str = user_id


class EqualSplit(Split):
    def __init__(self, user_id) -> None:
        super().__init__(user_id)

    def set_amount(self, amount):
        self.amount: float = amount


class ExactSplit(Split):
    def __init__(self, user_id, amount) -> None:
        super().__init__(user_id)
        self.amount: float = amount


class PercentSplit(Split):
    def __init__(self, user_id, percent) -> None:
        super().__init__(user_id)
        self.percent: float = percent


class PayerSplit(Split):
    def __init__(self, user_id, amount) -> None:
        super().__init__(user_id)
        self.amount: float = amount
