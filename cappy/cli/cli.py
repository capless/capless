import yaml
import os
class CappyCLI(object):

    def __init__(self):
        pass

    def write_config(self,file_name,options):
        os.makedirs(options['name'])
        with open(file_name, 'w+') as f:
            f.write(yaml.safe_dump(options, default_flow_style=False ))

    def create_project(self,options):
        self.write_config('{}/cappy.yaml'.format(options['name']),options)

