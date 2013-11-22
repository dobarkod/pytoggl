from datetime import datetime, timedelta, tzinfo
from mock import Mock
import pytest

from toggl.base import ObjectList, Object, cached_property


class MyTZ(tzinfo):
    def utcoffset(self, dt):
        return timedelta(minutes=7*60)
    def dst(self, dt):
        return 0
    def tzname(self, dt):
        return 'MyTZ'


class MyObject(Object):

    @cached_property
    def meaning_of_life(self):
        self.call_count += 1
        return 42


class MyObjectList(ObjectList):
    get_instance_cls = lambda self: MyObject
    url = None


def test_object_constructs_attribs_from_kwargs():
    o = MyObject(None, a=1, b='foo')

    assert o.a == 1
    assert o.b == 'foo'


def test_object_constructor_parses_json_datetime():
    o = MyObject(None, when='2001-02-03T04:05:06+07:00')

    assert isinstance(o.when, datetime)
    assert o.when == datetime(2001, 2, 3, 4, 5, 6, tzinfo=MyTZ())


def test_object_string_methods_returns_name_attribute():
    o = MyObject(None, name='mr.foo')

    assert str(o) == 'mr.foo'
    assert unicode(o) == u'mr.foo'

def test_object_parse_constructs_attribs_from_data():
    o = MyObject.parse(None, {'a': 1, 'b': 'foo'})

    assert o.a == 1
    assert o.b == 'foo'


def test_object_list_iteration_calls_get():
    api = Mock()
    api.session.get.return_value = [{'id': 1}, {'id': 2}]
    li = MyObjectList(api, url='http://example.com/foo')

    results = [el for el in li]

    api.session.get.assert_called_once_with('http://example.com/foo')
    assert len(results) == 2
    assert results[0].id == 1
    assert results[1].id == 2


def test_object_list_iteration_on_no_url_returns_nothing():
    api = Mock()
    li = MyObjectList(api)
    results = list(li)

    assert api.session.get.call_count == 0
    assert len(results) == 0


def test_object_list_iteration_caches_get_results():
    api = Mock()
    api.session.get.return_value = [{'id': 1}, {'id': 2}]
    li = MyObjectList(api, url='http://example.com/foo')

    [el for el in li]
    [el for el in li]

    api.session.get.assert_called_once_with('http://example.com/foo')


def test_object_list_instance_retrieval_errors_on_no_url():
    api = Mock()
    li = MyObjectList(api)

    with pytest.raises(AttributeError):
        li[42]


def test_object_list_instance_retrieval_calls_get():
    api = Mock()
    api.session.get.return_value = {'data': {'id': 42, 'name': 'foo'}}
    li = MyObjectList(api, url='http://example.com/foo')

    el = li[42]

    api.session.get.assert_called_once_with('http://example.com/foo/42')

    assert el.id == 42
    assert el.name == 'foo'


def test_object_list_caches_instances():
    api = Mock()
    api.session.get.return_value = {'data': {'id': 42, 'name': 'foo'}}
    li = MyObjectList(api, url='http://example.com/foo')

    li[42]
    li[42]

    api.session.get.assert_called_once_with('http://example.com/foo/42')


def test_cached_property_caches_function_return_value():

    o = MyObject(None)
    o.call_count = 0

    assert o.meaning_of_life == 42
    assert o.meaning_of_life == 42
    assert o.call_count == 1
