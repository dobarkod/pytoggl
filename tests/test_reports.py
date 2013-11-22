from datetime import date
from mock import patch
import pytest

from toggl.reports import Node, Reports


def test_node_construction_from_kwargs():
    n = Node(a=1, b=2)

    assert 'a' in n and 'b' in n
    assert sorted(n.keys) == ['a', 'b']
    assert n.a == 1
    assert n.b == 2


def test_node_construction_with_sublist():
    n = Node(a=[{'b': 1}, {'b': 2}])

    assert len(n.a) == 2
    assert n.a[0].b == 1
    assert n.a[1].b == 2


def test_node_construction_with_subdict():
    n = Node(a={'b': 1})
    assert n.a.b == 1


@patch('toggl.reports.Session')
def test_reports_request_with_workspace_specialization(Session):
    s = Session.return_value
    s.get.return_value = {'id': 1}

    r = Reports('api_token')
    r = r.for_workspace(42)

    n = r.weekly()

    s.get.assert_called_once_with('weekly',
        workspace_id=42, user_agent= Reports.USER_AGENT)

    assert n.id == 1


def test_reports_request_requires_workspace():
    r = Reports(None)

    with pytest.raises(ValueError):
        r.details()


@patch('toggl.reports.Session')
def test_reports_request_without_workspace_specialization(Session):
    s = Session.return_value
    s.get.return_value = {'id': 1}

    r = Reports('api_token')

    n = r.weekly(workspace_id=42)

    s.get.assert_called_once_with('weekly',
        workspace_id=42, user_agent= Reports.USER_AGENT)

    assert n.id == 1

@patch('toggl.reports.Session')
def test_reports_request_serializes_datetime(Session):
    s = Session.return_value
    r = Reports('api_token')

    r.details(workspace_id=42, when=date(2001, 1, 31))

    s.get.assert_called_once_with('details',
        workspace_id=42, user_agent= Reports.USER_AGENT,
        when='2001-01-31')


@patch('toggl.reports.Session')
def test_reports_summary_data_parsing(Session):
    s = Session.return_value
    s.get.return_value = {
        "total_grand": 42000,
        "total_billable": 21000,
        "total_currencies": [{"currency":"USD", "amount": 21000}],
        "data": [{
            "id": 1,
            "title": {"client": "Someone"},
            "time": 42000,
            "total_currencies": [{"currency": "USD", "amount": 21000}],
            "items": [{
                "title": {"user": "Worker"},
                "time":21000,
                "cur":"",
                "sum": None,
                "rate": None
            }]
        }]
    }

    r = Reports('api_token')
    data = r.summary(workspace_id=42)

    assert data.total.grand == 42
    assert data.total.billable == 21
    assert len(data.total.currencies) == 1
    assert data.total.currencies[0].currency == 'USD'
    assert len(data.groups) == 1
    assert data.groups[0].id == 1
    assert data.groups[0].title == u'Someone'
    assert data.groups[0].time == 42
    assert len(data.groups[0].subgroups) == 1
    assert data.groups[0].subgroups[0].title == 'Worker'
    assert data.groups[0].subgroups[0].time == 21
