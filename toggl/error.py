
class Error(Exception):

    def __init__(self, message=None, response=None):
        if response is not None:
            self.status_code = response.status_code
            if response.headers.get('content-type') == 'application/json':
                json_error = response.json()
                if isinstance(json_error, dict):
                    self.message = json_error.get('message', '')
                elif isinstance(json_error, list):
                    self.message = ', '.join(json_error)
                else:
                    self.message = response.text.strip()
            else:
                self.message = response.text.strip()
        else:
            self.status_code = 0
            self.message = message

    def __str__(self):
        return str(self.message)

    def __unicode__(self):
        return unicode(self.message)
