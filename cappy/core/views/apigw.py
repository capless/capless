import paginate

from . import Mixin,View
from ..loading.templates import env
from .events import APIGWEvent


class TemplateMixin(Mixin):
    content_type = 'text/html'
    template_name = 'base.html'
    request_method_names = [
        'get', 'post', 'head', 'delete',
        'put', 'patch', 'trace', 'options']
    event_type = APIGWEvent

    def get_template(self):
        return env.get_template(self.template_name)

    def get(self):
        context = self.get_context()
        template = env.get_template(self.template_name)
        return template.render(**context)


class TemplateView(TemplateMixin,View):
    pass


class ObjectMixin(object):
    model_class = None
    id_attribute = 'slug'

    def get_object(self):
        id_value = self.event.path_vars.get(self.id_attribute)
        pk = self.event.path_vars.get('pk')
        if not id_value and not pk:
            raise ValueError('KevObjectMixins require either an id_value ("slug") or pk value.')
        if id_value:
            return self.model_class.objects().get({self.id_attribute:id_value})

        return self.model_class.get(pk)


class ObjectView(TemplateMixin,ObjectMixin,View):

    def get_context(self,**kwargs):
        context = super(ObjectView, self).get_context(**kwargs)
        context['object'] = self.get_object()
        return context


class MultiObjectMixin(ObjectMixin):
    paginate_by = None
    filters = None
    def get_filters(self):
        return self.filters

    def get_object_list(self):
        filters = self.get_filters()
        if filters:
            return self.model_class.objects().filter(filters)
        return self.model_class.all()

    def get_object_list_paginated(self):
        return paginate.Page(self.get_object_list(),
                             items_per_page=self.paginate_by,
                             page=self.get_page_number())

    def get_page_number(self):
        return self.event.path_vars.get('page',self.event.querystring.get('page'))

class MultiObjectView(TemplateMixin,MultiObjectMixin,View):


    def get_context(self,**kwargs):
        context = super(ObjectView, self).get_context(**kwargs)
        if self.paginate_by:
            context['object_list'] = self.get_object_list_paginated()
        else:
            context['object_list'] = self.get_object_list()
        return context
