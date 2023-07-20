from exceptions import AlreadyExists, DoesNotExists
from repository import utils
from models.bill import Bill


class BillRepo:
    def __init__(self) -> None:
        self.bills = {}

    def add(self, bill) -> None:
        if bill.id:
            raise AlreadyExists("bill already has an id")
        bill.id = utils.gen_id()
        self.bills[bill.id] = bill

    def get(self, id) -> Bill:
        if not self.bills.get(id):
            raise DoesNotExists("bill with given id does not exists")
        return self.bills[id]
