from api import schema
from models.group import Group


def group_to_response(group: Group) -> schema.GroupResponse:
    return schema.GroupResponse(
        id=group.id,
        name=group.name,
        creator_id=group.created_by.id,
        participants=[
            schema.UserResponse(id=user.id, name=user.name, email=user.email)
            for user in group.participants
        ],
    )
