from envs import env

from cappy.utils import import_mod, import_util


class Event(object):

    def __init__(self,event,context):
        pass


class APIGWEvent(Event):

    def __init__(self,event,context):
        self.body = event['body']
        self.resource = event['resource']
        self.http_method = event['httpMethod']
        self.path_params = event['pathParameters']
        self.headers = event['headers']
        self.stage_vars = event['stageVariables']
        self.path = event['path']
        self.is_base64_encoded = event['isBase64Encoded']
        self.query_string_params = event['queryStringParameters']


class Response(object):
    pass


