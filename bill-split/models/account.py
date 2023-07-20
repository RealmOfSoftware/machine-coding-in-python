class User:
    def __init__(self, name: str, email: str):
        self.id = None
        self.name = name
        self.email = email


class UserBalance:
    def __init__(self, user: User, amount: float) -> None:
        self.user = user
        self.amount = amount
