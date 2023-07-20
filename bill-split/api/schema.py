from pydantic import BaseModel

from models.split import SplitType


class UserRequest(BaseModel):
    "Create user request schema"
    name: str
    email: str


class UserResponse(UserRequest):
    id: str


class GroupRequest(BaseModel):
    "Create group request schema"
    name: str
    creator_id: str


class GroupResponse(GroupRequest):
    id: str
    participants: list[UserResponse] = []


class PayerSplitRequest(BaseModel):
    user_id: str
    amount: float


class SplitRequest(BaseModel):
    "Split request schema, either of amount or percent should be provided based on type"
    user_id: str
    amount: float | None = None
    percent: float | None = None


class BillRequest(BaseModel):
    "Create bill request schema"
    split_type: SplitType
    title: str
    amount: float
    payers: list[PayerSplitRequest]
    splits: list[SplitRequest]


class BillResponse(BillRequest):
    id: str


class UserBalance(BaseModel):
    user_id: str
    amount: float


class UserBalanceResponse(BaseModel):
    total_balance: float
    balances: list[UserBalance]
