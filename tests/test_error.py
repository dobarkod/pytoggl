from mock import Mock

from toggl.error import Error


def test_error_picks_up_message_and_serves_as_string_value():
    ex  = Error(message='foo')
    assert str(ex) == 'foo'
    assert unicode(ex) == u'foo'

def test_error_picks_up_status_code_message_from_response_body():
    response = Mock(status_code=403, text='foo')

    ex = Error(response=response)
    assert ex.status_code == 403
    assert str(ex) == 'foo'


def test_error_picks_up_message_from_json_if_response_content_type_is_json():
    response_json = Mock(return_value={'message': 'foo'})
    response = Mock(status_code=403, json=response_json, headers={
        'content-type': 'application/json'})

    ex = Error(response=response)
    assert ex.status_code == 403
    assert str(ex) == 'foo'

def test_error_picks_up_message_list():
    response_json = Mock(return_value=['One', 'Two', 'Three'])
    response = Mock(status_code=403, json=response_json, headers={
        'content-type': 'application/json'})

    ex = Error(response=response)
    assert str(ex) == 'One, Two, Three'

