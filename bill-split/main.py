from models.split import EqualSplit, ExactSplit, PayerSplit, PercentSplit, SplitType
from repository.balance import UserBalanceRepo
from repository.bill import BillRepo
from repository.group import GroupRepo
from repository.user import UserRepo
from services.bill import BillService
from services.group import GroupService
from services.user import UserService


def test_bill():
    user_repo = UserRepo()
    balance_repo = UserBalanceRepo()
    group_repo = GroupRepo()
    bill_repo = BillRepo()
    user_service = UserService(user_repo, balance_repo)
    group_service = GroupService(group_repo, user_repo)
    bill_service = BillService(bill_repo, user_repo, group_repo, balance_repo)
    user1 = user_service.register_user("user1", "u1@example.com")
    user2 = user_service.register_user("user2", "u2@example.com")
    user3 = user_service.register_user("user3", "u3@example.com")
    group = group_service.create_group("group1", user1.id)
    group.add_participant(user1)
    group.add_participant(user2)
    group.add_participant(user3)
    bill1 = bill_service.create_group_bill(
        group.id,
        SplitType.EXACT,
        "bill1",
        100,
        [PayerSplit(user1.id, 60), PayerSplit(user2.id, 40)],
        [ExactSplit(user1.id, 40), ExactSplit(user2.id, 30), ExactSplit(user3.id, 30)],
    )
    bill2 = bill_service.create_group_bill(
        group.id,
        SplitType.PERCENT,
        "bill2",
        100,
        [PayerSplit(user1.id, 60), PayerSplit(user2.id, 40)],
        [
            PercentSplit(user1.id, 40),
            PercentSplit(user2.id, 30),
            PercentSplit(user3.id, 30),
        ],
    )
    bill3 = bill_service.create_group_bill(
        group.id,
        SplitType.EQUAL,
        "bill3",
        100,
        [PayerSplit(user1.id, 60), PayerSplit(user2.id, 40)],
        [EqualSplit(user1.id), EqualSplit(user2.id), EqualSplit(user3.id)],
    )

    # print("balances", balance_repo.balances)

    users = [user1, user2, user3]
    balances = {user.name: user_service.get_balances(user.id) for user in users}
    for user_name in balances:
        print(f"balance for {user_name}: ")
        for balance in balances[user_name]:
            if balance.amount > 0:
                print(f"    - {balance.user.name} owes {balance.amount}")
            else:
                print(f"    - {balance.user.name} owed {-balance.amount}")


if __name__ == "__main__":
    test_bill()
