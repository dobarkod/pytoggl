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
            yield self.get_instance_cls().parse(self.api, data)

    def get(self, object_id):
        return self[object_id]

    def __getitem__(self, object_id):
        if self.url is None:
            raise AttributeError('URL is not set')

        if object_id not in self._instance_cache:
            data = self.api.session.get('%s/%d' % (self.url, object_id))
            if data and 'data' in data and data['data'] is not None:
                self._instance_cache[object_id] = \
                    self.get_instance_cls().parse(self.api, data['data'])
            else:
                raise IndexError("%s with id %d doesn't exist" %
                    (self.get_instance_cls().__name__, object_id))

        return self._instance_cache[object_id]


class Object(object):

    def __init__(self, api, **kwargs):
        self.api = api
        for k, v in kwargs.iteritems():
            try:
                v = iso8601.parse_date(v)
                kwargs[k] = v
            except iso8601.iso8601.ParseError:
                pass

        self.__dict__.update(kwargs)

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return str(self.name)

    @classmethod
    def parse(cls, api, data):
        return cls(api, **data)


def cached_property(fn):
    cache_name = '_' + fn.__name__ + '_cache'
    def wrapper(self):
        if not hasattr(self, cache_name):
            setattr(self, cache_name, fn(self))
        return getattr(self, cache_name)
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return property(wrapper)
