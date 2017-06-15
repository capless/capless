import jinja2
import os
import yaml


from capless.core.exceptions import CappyInitializeError


CLI_TEMPLATES = jinja2.Environment(loader=jinja2.PackageLoader(
    'capless','templates'))

class CaplessCLI(object):

    def __init__(self):
        pass

    def write_config(self,file_name,options):
        os.makedirs(options['name'])
        with open(file_name, 'w+') as f:
            f.write(yaml.safe_dump(options, default_flow_style=False ))

    def update_config(self,file_name,update_attr,options,file_required=False):
        try:
            with open(file_name,'r') as f:
                config = yaml.safe_load(f)
                config[update_attr].append(options['name'])
                unique_attr = list(set(config[update_attr]))
                config[update_attr] = unique_attr
            with open(file_name,'w+') as f:
                f.write(yaml.safe_dump(config, default_flow_style=False))
        except FileNotFoundError:
            if file_required:
                raise CappyInitializeError(
                    'Your current directory does not have the required '
                    '{} file.'.format(file_name))

    def create_project(self,options):
        self.write_config('{}/capless.yaml'.format(options['name']),options)

    def create_app_files(self,options):
        app_name = options.get('name')
        #Create templates folder
        temp_dir = '{}/templates/'.format(app_name)
        os.makedirs(temp_dir)

        html_template = CLI_TEMPLATES.get_template('base.html')
        with open('{}base.html'.format(temp_dir),'w+') as f:
            f.write(html_template.render(app_name=app_name))

        #Create views.py
        view_template = CLI_TEMPLATES.get_template('views.jinja2')
        with open('{}/views.py'.format(app_name),'w+') as f:
            f.write(view_template.render(app_name=app_name))

        #Create app.py
        app_template = CLI_TEMPLATES.get_template('app.py.jinja2')
        with open('{}/app.py'.format(app_name),'w+') as f:
            f.write(app_template.render(app_name=app_name))

        # Create urls.py
        urls_template = CLI_TEMPLATES.get_template('urls.py.jinja2')
        with open('{}/urls.py'.format(app_name), 'w+') as f:
            f.write(urls_template.render(app_name=app_name))

        #Create __init__.py
        with open('{}/__init__.py'.format(app_name),'w+') as f:
            f.write('')

    def create_app(self,options):
        self.update_config('capless.yaml','apps',options)
        self.write_config('{}/app.yaml'.format(options['name']),options)
        self.create_app_files(options)

    def create_function(self,options):

        self.write_config('{}/function.yaml'.format(options['name']),options)

