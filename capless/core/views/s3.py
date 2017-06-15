from . import Mixin,View


class S3(Mixin,View):
    request_type = 'core.requests.S3Request'
    trigger = 'S3'
