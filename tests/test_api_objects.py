from mock import patch, MagicMock

from toggl.api import Api
from toggl.client import Client
from toggl.project import Project, ProjectList, ProjectUser, ProjectUserList
from toggl.user import UserList
from toggl.workspace import Workspace


@patch('toggl.api.Session')
def test_api_setup(Session):
    Api('token')

    Session.assert_called_once_with(Api.BASE_URL, 'token')

def test_client_workspace_attr_triggers_workspace_get():
    api = MagicMock()

    c = Client(api, wid=42)
    w = c.workspace

    api.workspaces.__getitem__.assert_called_once_with(42)
    assert w == api.workspaces.__getitem__.return_value


def test_client_projects_attr_returns_project_list():
    c = Client(None, id=1)
    p = c.projects

    assert type(p) == ProjectList
    assert p.url == 'clients/1/projects'


def test_project_users_attr_returns_project_user_list():
    p = Project(None, id=1)
    u = p.project_users

    assert type(u) == ProjectUserList
    assert u.url == 'projects/1/project_users'


def test_project_user_user_attr_triggers_user_get():
    api = MagicMock()

    pu = ProjectUser(api, wid=42, uid=1)
    pu.user

    api.workspaces.__getitem__.assert_called_once_with(42)
    ws = api.workspaces.__getitem__.return_value
    ws.users.__getitem__.assert_called_once_with(1)


def test_workspace_users_returns_user_list():
    w = Workspace(None, id=1)
    u = w.users

    assert type(u) == UserList
    assert u.url == 'workspaces/1/users'

def test_workspace_reports_returns_reports_factory():
    api = MagicMock()

    w = Workspace(api, id=1)
    r = w.reports

    api.reports.for_workspace.assert_called_once_with(1)
    assert r == api.reports.for_workspace.return_value
