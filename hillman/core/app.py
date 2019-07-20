
from capless.utils import import_util
from capless.core.events import APIGWEvent


def get_url(url_config,resource):
    def url_filter(url):
        if url.resource == resource:
            return url
    return filter(url_filter,url_config)


class App(object):

    def __init__(self,url_config):
        self.url_config = import_util(url_config)

    def run_event_middleware(self,event):
        return event

    def run_reponse_middleware(self,response):
        return response

    def get_view(self):
        url = tuple(get_url(self.url_config,self.event.resource))
        return url[0].view

    def __call__(self, event_dict, context):
        self.context = context
        self.event = APIGWEvent(event_dict)
        response = self.get_view().as_function()(self.event,self.context)
        return response