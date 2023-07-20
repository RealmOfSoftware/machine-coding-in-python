from models.group import Group


class GroupService:
    def __init__(self, group_repo, user_repo) -> None:
        self.group_repo = group_repo
        self.user_repo = user_repo

    def create_group(self, name: str, creator_id: str) -> Group:
        creator = self.user_repo.get(creator_id)
        group = Group(name, creator)
        self.group_repo.add(group)
        return group

    def add_participant(self, group_id: str, user_id: str) -> Group:
        user = self.user_repo.get(user_id)
        group = self.group_repo.get(group_id)
        group.add_participant(user)
        return group
