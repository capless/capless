from cappy.utils import import_util

class URL(object):

    def __init__(self,path_string,view_string,name,**kwargs):
        self.path_string = path_string
        self.view_string = view_string
        self.view = import_util(self.view_string)
        self.name = name

    def reverse(self,**kwargs):
        return self.path_string.format(**kwargs)


