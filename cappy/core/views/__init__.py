from .events import Event

class Mixin(object):

    def get_context(self,**kwargs):
        return {
            'event':self.event,
            'context':self.context
        }

class View:
    event_type = None

    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)

    @classmethod
    def as_function(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        def func(event_dict,context):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.event_dict = event_dict
            self.context = context
            return self.dispatch(event_dict, context)
        return func


    def dispatch(self, event_dict, context):
        self.event = self.event_type(event_dict)
        self.context = context
        method = getattr(self,self.event.method)
        return method()