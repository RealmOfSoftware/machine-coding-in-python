from typing import List

from models.account import User, UserBalance


class UserService:
    def __init__(self, user_repo, balance_repo) -> None:
        self.user_repo = user_repo
        self.balance_repo = balance_repo

    def register_user(self, name: str, email: str) -> User:
        user = User(name, email)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User:
        return self.user_repo.get(user_id)

    def get_balance_between(self, owner_user_id, target_user_id) -> float:
        return self.balance_repo.get_balance(owner_user_id).get(target_user_id, 0)

    def get_my_owed_balance(self, user_id) -> float:
        all_balances = self.balance_repo.get_balances(user_id)
        balance = sum([all_balances[uid] for uid in all_balances])
        return balance

    def get_balances(self, user_id) -> List[UserBalance]:
        all_balances = self.balance_repo.get_balances(user_id)
        balances = [
            UserBalance(self.user_repo.get(user_id), all_balances[user_id])
            for user_id in all_balances
        ]
        return balances
