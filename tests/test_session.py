from mock import Mock, patch
import pytest

from toggl.session import Session
from toggl.error import Error


@patch('toggl.session.requests')
def test_session_setup(requests):
    session = requests.Session.return_value
    session.headers = {}

    s = Session('http://example.com/', 'my-secret-token')

    requests.Session.assert_called_once_with()
    assert session.auth == ('my-secret-token', 'api_token')
    assert session.headers['content-type'] == 'application/json'
    assert s.session == session


@patch('toggl.session.requests')
def test_session_get_calls_requests_session_get(requests):
    session = requests.Session.return_value
    session.get.return_value = Mock(status_code=200)
    session.get.return_value.json.return_value = {}

    s = Session('http://example.com/', 'my-secret-token')
    resp = s.get('foo', bar=1, baz='x y')

    session.get.assert_called_once_with(
        'http://example.com/foo', params={
            'bar': 1,
            'baz': 'x y'
        })

    assert resp == {}


@patch('toggl.session.requests')
def test_session_get_throws_error_on_error_response(requests):
    session = requests.Session.return_value
    session.get.return_value = rv = Mock(status_code=400)
    rv.headers = {'content-type': 'application/json'}
    rv.json.return_value = {'message': 'invalid request'}

    s = Session('http://example.com/', 'my-secret-token')

    with pytest.raises(Error) as e:
        s.get('foo')

    assert e.value.status_code == 400
    assert e.value.message == 'invalid request'


@patch('toggl.session.requests')
def test_session_get_throws_error_on_requets_error(requests):
    session = requests.Session.return_value
    session.get.side_effect = Exception('oh noez!')

    s = Session('http://example.com/', 'my-secret-token')

    with pytest.raises(Error) as e:
        s.get('foo')

    assert e.value.status_code == 0
    assert e.value.message == 'oh noez!'


@patch('toggl.session.requests')
def test_session_get_throws_error_on_non_json_response(requests):
    session = requests.Session.return_value
    session.get.return_value = Mock(status_code=200)
    session.get.return_value.json.side_effect = Exception('not a json!')

    s = Session('http://example.com/', 'my-secret-token')

    with pytest.raises(Error) as e:
        s.get('foo')

    assert e.value.status_code == 0
    assert e.value.message == 'not a json!'
