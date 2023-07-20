from repository import utils
from exceptions import AlreadyExists, DoesNotExists


class UserRepo:
    def __init__(self):
        self.users = {}

    def add(self, user):
        if user.id or user.email in self.users:
            raise AlreadyExists("user already have an id")
        user.id = user.email
        self.users[user.id] = user

    def get(self, id):
        if not self.users.get(id):
            raise DoesNotExists("user with given id does not exists")
        return self.users[id]
