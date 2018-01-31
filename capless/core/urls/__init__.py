from ...utils import import_util


class URL(object):

    def __init__(self,resource,view_string,name,**kwargs):
        self.resource = resource
        self.view_string = view_string
        self.view = import_util(self.view_string)
        self.name = name

    def reverse(self,**kwargs):
        return self.resource.format(**kwargs)


