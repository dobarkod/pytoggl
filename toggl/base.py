import iso8601

__all__ = ['ObjectList', 'Object', 'cached_property']


class ObjectList(object):

    get_instance_cls = None
    url = None

    def __init__(self, api, url=None):
        if url is not None:
            self.url = url
        self.api = api
        self._instance_cache = {}

    def list(self):
        return list(self)

    def __iter__(self):
        if self.url is None:
            raise StopIteration

        if not hasattr(self, '_datalist'):
            self._datalist = self.api.session.get(self.url)

        for data in self._datalist:
            yield self.get_instance_cls()(self.api, **data)

    def get(self, object_id):
        return self[object_id]

    def __getitem__(self, object_id):
        if self.url is None:
            raise AttributeError('URL is not set')

        if object_id not in self._instance_cache:
            data = self.api.session.get('%s/%d' % (self.url, object_id))
            if data and 'data' in data and data['data'] is not None:
                self._instance_cache[object_id] = \
                    self.get_instance_cls()(self.api, **data['data'])
            else:
                raise IndexError("%s with id %d doesn't exist" %
                    (self.get_instance_cls().__name__, object_id))

        return self._instance_cache[object_id]

    def create(self, **kwargs):
        obj = self.get_instance_cls()(self.api, **kwargs)
        obj.save()
        self._instance_cache[obj.id] = obj
        return obj


class Object(object):

    def __init__(self, api, **kwargs):
        self.api = api
        self.id = None
        self._update_attrs(kwargs)

    def _update_attrs(self, attrs):
        for k, v in attrs.iteritems():
            try:
                v = iso8601.parse_date(v)
                attrs[k] = v
            except iso8601.iso8601.ParseError:
                pass
        self.__dict__.update(attrs)

    def _serialize_attrs(self, attrs):
        from datetime import date, datetime
        data = {}
        for k, v in attrs.items():
            if k in ['api']:
                continue
            if isinstance(v, date):
                v = v.strftime('%Y-%m-%d')
            elif isinstance(v, datetime):
                v = v.strftime('%Y-%m-%dT%H:%M:%S')
            data[k] = v
        return data

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return str(self.name)

    def get_instance_url(self):
        return None

    def to_dict(self, data):
        return data

    def delete(self):
        url = self.get_instance_url()
        if not url:
            raise IndexError("%s can't be deleted", self.__class__.__name__)
        self.api.session.delete(url)

    def save(self):
        data = self.to_dict(self._serialize_attrs(self.__dict__))
        url = self.get_instance_url()

        if self.id:
            response = self.api.session.put(url, data)
        else:
            response = self.api.session.post(url, data)

        if response and 'data' in response and response['data'] is not None:
            self._update_attrs(response['data'])

        return self


def cached_property(fn):
    cache_name = '_' + fn.__name__ + '_cache'
    def wrapper(self):
        if not hasattr(self, cache_name):
            setattr(self, cache_name, fn(self))
        return getattr(self, cache_name)
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return property(wrapper)
