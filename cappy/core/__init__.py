from envs import env

from cappy.utils import import_mod, import_util


class Request(object):

    def __init__(self,event,context):
        pass


class APIGWRequest(Request):

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

# ('Event',
#     {u'body': None, u'resource': u'/{proxy+}',
#      u'requestContext': {u'resourceId': u'ff744h', u'apiId': u'pbp4dlwi42', u'resourcePath': u'/{proxy+}',
#                          u'httpMethod': u'GET', u'requestId': u'test-invoke-request', u'accountId': u'986625141461',
#                          u'identity': {u'apiKey': u'test-invoke-api-key', u'userArn': u'arn:aws:iam::986625141461:root',
#                                        u'cognitoAuthenticationType': None, u'accessKey': u'ASIAJ3GZ7YEE6R5JTZAQ',
#                                        u'caller': u'986625141461', u'userAgent': u'Apache-HttpClient/4.5.x (Java/1.8.0_102)',
#                                        u'user': u'986625141461', u'cognitoIdentityPoolId': None,
#                                        u'cognitoIdentityId': None, u'cognitoAuthenticationProvider': None,
#                                        u'sourceIp': u'test-invoke-source-ip', u'accountId': u'986625141461'},
#                          u'stage': u'test-invoke-stage'},
#      u'queryStringParameters': {u'and': u'teacher', u'good': u'father'},
#      u'httpMethod': u'GET',
#      u'pathParameters': {u'proxy': u'rip/darryl-roberts'},
#      u'headers': None,
#      u'stageVariables': None,
#      u'path': u'/rip/darryl-roberts/',
#      u'isBase64Encoded': False}
#  )

class Response(object):
    pass


class Cappy(object):
    def __init__(self):
        self.settings = import_mod(env('CAPPY_SETTINGS_MODULE'))
        self.url_config = self.settings.URL_CONFIG

    def get_request(self):
        pass

