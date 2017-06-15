from capless.utils import import_util


class App(object):

    def __init__(self,url_config):
        self.url_config = import_util(url_config)

    def __call__(self, event, context):
        url_path = event.get()