from typing import Annotated
from fastapi import APIRouter, Body

from repository.balance import UserBalanceRepo
from repository.bill import BillRepo
from repository.group import GroupRepo
from repository.user import UserRepo
from services.bill import BillService
from services.group import GroupService
from services.user import UserService
from api import schema, conv


user_repo = UserRepo()
balance_repo = UserBalanceRepo()
group_repo = GroupRepo()
bill_repo = BillRepo()
user_service = UserService(user_repo, balance_repo)
group_service = GroupService(group_repo, user_repo)
bill_service = BillService(bill_repo, user_repo, group_repo, balance_repo)

router = APIRouter()


@router.post("/users", response_model=schema.UserResponse, status_code=201)
def create_user(user: schema.UserRequest):
    user = user_service.register_user(user.name, user.email)
    return user


@router.post("/groups", response_model=schema.GroupResponse, status_code=201)
def create_group(group: schema.GroupRequest):
    group = group_service.create_group(group.name, group.creator_id)
    return conv.group_to_response(group)


@router.post("/groups/{group_id}/participants", response_model=schema.GroupResponse)
def add_participant_to_group(group_id: str, user_id: Annotated[str, Body(embed=True)]):
    group = group_service.add_participant(group_id, user_id)
    return conv.group_to_response(group)


@router.post("/bills", response_model=schema.BillResponse, status_code=201)
def create_bill(bill: schema.BillRequest):
    if bill.group_id:
        bill = bill_service.create_group_bill(
            bill.group_id,
            bill.split_type,
            bill.title,
            bill.amount,
            bill.payers,
            bill.splits,
        )
    else:
        bill = bill_service.create_bill(
            bill.split_type, bill.title, bill.amount, bill.payers, bill.splits
        )
    return bill


@router.get("/users/{user_id}/balances")
def get_balance(user_id) -> schema.UserBalanceResponse:
    balances = user_service.get_balances(user_id)
    total_balance = user_service.get_my_owed_balance(user_id)
    return schema.UserBalanceResponse(
        total_balance=total_balance,
        balances=[
            schema.UserBalance(user_id=b.user.id, amount=b.amount) for b in balances
        ],
    )
