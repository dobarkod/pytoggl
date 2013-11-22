from .base import ObjectList, Object, cached_property

__all__ = ['ClientList', 'Client']


class ClientList(ObjectList):
    """A collection of Clients."""

    get_instance_cls = lambda self: Client
    url = 'clients'


class Client(Object):
    """Client object.

    API doc: https://github.com/toggl/toggl_api_docs/blob/master/chapters/clients.md

    """
    @cached_property
    def workspace(self):
        return self.api.workspaces[self.wid]

    @cached_property
    def projects(self):
        from .project import ProjectList

        return ProjectList(self.api,
            url='clients/%d/projects' % self.id)
