from .base import ObjectList, Object, cached_property

__all__ = ['WorkspaceList', 'Workspace']


class WorkspaceList(ObjectList):
    get_instance_cls = lambda self: Workspace
    url = 'workspaces'


class Workspace(Object):

    @cached_property
    def users(self):
        from .user import UserList
        return UserList(self.api, url='workspaces/%d/users' % self.id)

    @cached_property
    def reports(self):
        return self.api.reports.for_workspace(self.id)

    @cached_property
    def projects(self):
        from .project import ProjectList
        return ProjectList(self.api, url='workspaces/%d/projects' % self.id)

    @cached_property
    def tasks(self):
        from .task import TaskList
        return TaskList(self.api, url='workspaces/%d/tasks' % self.id)
