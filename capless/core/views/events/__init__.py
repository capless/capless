class Event(object):
    method = 'main'

    def __init__(self, event_dict):
        self.event_dict = event_dict


class APIGWEvent(Event):

    def __init__(self ,event_dict):
        super(APIGWEvent, self).__init__(event_dict)
        self.body = self.event_dict.get('body-json')
        self.headers = self.event_dict.get('params',dict()).get('header')
        self.path_vars = self.event_dict.get('params',dict()).get('path')
        self.querystring = self.event_dict.get('params',dict()).get('querystring')
        self.context = self.event_dict.get('context')
        self.method = self.context.get('http-method').lower()
