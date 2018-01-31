from capless.core.events import Event


class Mixin(object):

    def get_context(self,**kwargs):
        return {
            'event':self.event,
            'context':self.context
        }


class View:

    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)

    @classmethod
    def as_function(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        def func(event,context):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.event = event
            self.context = context
            return self.dispatch(event, context)
        return func


    def dispatch(self, event, context):
        self.context = context
        method = getattr(self,self.event.method)
        return method()