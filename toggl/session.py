import requests
from urllib import urlencode
import logging

from .error import Error

log = logging.getLogger(__name__)

class Session(object):

    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (api_token, 'api_token')
        self.session.headers['content-type'] = 'application/json'

    def _exec(self, method, url, *args, **kwargs):
        try:
            log.debug("[req]: %s?%s" % (self.base_url + url,
                urlencode(kwargs.get('params'))))
            response = method(self.base_url + url, *args, **kwargs)
            log.debug("[resp %d]: %s" % (response.status_code,
                repr(response.text)))
        except Exception as ex:
            print "HERE!", repr(ex)
            log.debug("[err]: %s" % str(ex))
            raise Error(str(ex))

        if (response.status_code // 100) != 2:
            raise Error(response=response)

        try:
            return response.json()
        except Exception as ex:
            log.debug("[err]: error parsing JSON response: " + str(ex))
            raise Error(str(ex))

    def get(self, url, **params):
        return self._exec(self.session.get, url, params=params)
