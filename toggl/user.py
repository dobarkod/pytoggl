from .base import ObjectList, Object

__all__ = ['UserList', 'User']


class UserList(ObjectList):
    get_instance_cls = lambda self: User


class User(Object):

    @property
    def name(self):
        return self.fullname

