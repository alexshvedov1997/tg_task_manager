class UserAlreadyExist(Exception):
    """User with current chat_id already exist"""


class UserNotFound(Exception):
    """User doesn't exist in the db"""


class TaskNotFound(Exception):
    """Task doesn't exist in the db"""
