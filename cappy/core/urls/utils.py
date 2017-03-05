from envs import env

from cappy.utils import import_util


def reverse_url_list(name):
    url_list = filter((lambda x: x.name == name), import_util(env('URL_PATTERNS')))
    if len(url_list) == 1:
        return url_list[0]
    if len(url_list) == 0:
        raise ValueError('URL Not Found')
    if len(url_list) > 1:
        raise ValueError('Multiple URLs found for name given')


def reverse(name, **kwargs):
    url = reverse_url_list(name)
    app_prefix = env('URL_PREFIX')
    return '{}{}'.format(app_prefix,url.reverse(**kwargs))
