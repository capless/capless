class Event(object):
    method = 'main'

    def __init__(self, event):
        self.event_dict = event


class APIGWEvent(Event):

    def __init__(self ,event):
        super(APIGWEvent, self).__init__(event)
        self.body = event['body']
        self.resource = event['resource']
        self.request_context = event['requestContext']
        self.query_string_params = event['queryStringParameters']
        self.path_params = event['pathParameters']
        self.headers = event['headers']
        self.method = event['httpMethod'].lower()
        self.stage_vars = event['stageVariables']
        self.path = event['path']


