from .session import Session

__all__ = ['Api']


class Api(object):

    BASE_URL = 'https://toggl.com/api/v8/'

    def __init__(self, api_token):
        from .client import ClientList
        from .workspace import WorkspaceList
        from .project import ProjectList
        from .reports import Reports

        self.session = Session(self.BASE_URL, api_token)
        self.clients = ClientList(self)
        self.workspaces = WorkspaceList(self)
        self.projects = ProjectList(self)
        self.reports = Reports(api_token)
