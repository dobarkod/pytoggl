from .base import ObjectList, Object

__all__ = ['TaskList', 'Task']


class TaskList(ObjectList):
    """A collection of Tasks."""

    get_instance_cls = lambda self: Task
    url = 'tasks'


class Task(Object):
    """Task object:

    API doc: https://github.com/toggl/toggl_api_docs/blob/master/chapters/tasks.md

    """

    def get_instance_url(self):
        return 'tasks/%d' % self.id if self.id else 'tasks'

    def to_dict(self, attrs):
        return {'task': attrs}
