from exceptions import AlreadyExists, DoesNotExists

from repository import utils
from models.group import Group


class GroupRepo:
    def __init__(self) -> None:
        self.groups = {}

    def add(self, group: Group) -> None:
        if group.id:
            raise AlreadyExists("group already have an id")
        group.id = utils.gen_id()
        self.groups[group.id] = group

    def get(self, id) -> Group:
        if not self.groups.get(id):
            raise DoesNotExists("group with given id does not exists")
        return self.groups[id]
