class UserBalanceRepo:
    def __init__(self) -> None:
        self.balances = {}

    def get_balances(self, user_id: str) -> dict:
        user_balances = self.balances.get(user_id, {})
        return user_balances

    def set_balance(self, owner_user_id, target_user_id, amount) -> None:
        if not self.balances.get(owner_user_id):
            self.balances[owner_user_id] = {}

        if not self.balances[owner_user_id].get(target_user_id):
            self.balances[owner_user_id][target_user_id] = 0

        self.balances[owner_user_id][target_user_id] += amount
