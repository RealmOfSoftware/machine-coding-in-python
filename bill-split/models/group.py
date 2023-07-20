from exceptions import AlreadyExists
from models.account import User
from models.bill import Bill


class Group:
    def __init__(self, name: str, creator: User) -> None:
        self.id = None
        self.name: str = name
        self.created_by: User = creator
        self.participants: list[User] = []
        self.bills: list[Bill] = []

    def add_participant(self, user: User) -> None:
        if user in self.participants:
            raise AlreadyExists("user already exists in group")

        self.participants.append(user)

    def remove_participants(self, user) -> None:
        pass

    def get_bills(self, offset, limit):
        return self.bills[offset : offset + limit]

    def add_bill(self, bill):
        return self.bills.append(bill)
