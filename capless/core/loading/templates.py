from jinja2 import BaseLoader, TemplateNotFound, Environment, FileSystemLoader
from kev.loading import KevHandler
from envs import env
from kev import Document, CharProperty, DateTimeProperty


kev_handler = KevHandler({
    'templates': {
        'backend': 'kev.backends.s3.db.S3DB',
        'connection': {
            'bucket': env('KEV_TEMPLATES_BUCKET')
        }
    }
})


class Template(Document):
    name = CharProperty(required=True, index=True, unique=True)
    body = CharProperty(required=True)
    last_modified = DateTimeProperty(auto_now=True)

    class Meta:
        use_db = 'templates'
        handler = kev_handler


class KevLoader(BaseLoader):
    def get_source(self, environment, template):
        t = Template.objects().filter({'name': template})
        try:
            def get_last_mod():
                return t[0].last_modified

            return t[0].body, t[0].name, get_last_mod
        except IndexError:
            raise TemplateNotFound(template)


env = Environment(
    loader=FileSystemLoader(env('TEMPLATES_PATH'))
)