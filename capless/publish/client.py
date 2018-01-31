import os
import shutil

import boto3
import pip
import yaml

import sammy as sm
from awscli.customizations.cloudformation.exceptions import ChangeEmptyError

from capless.utils import import_util

s3 = boto3.client('s3')

class Publish(object):

    config_path = 'capless.yaml'
    venv = '_venv'
    requirements_filename = 'requirements.txt'

    def __init__(self,config=None,config_path=None):

        self.config = config or self.load_config(config_path)
        self.project_name = self.config.get('name')

    def load_config(self,config_path):
        with open(config_path or self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def publish_app(self,app_name,stage_name):

        stage_settings = self.config['stages'][stage_name]
        self.copy_app_files(app_name)
        self.copy_capless(app_name)
        self.install_packages(app_name,self.get_requirements_path(app_name))
        self.build_zip(app_name,self.get_zip_name(app_name,stage_name,no_ext=True))
        #Upload zip and return its path
        bucket,zip_name = self.upload_zip(self.get_zip_name(app_name,stage_name),stage_settings)
        self.remove_build_artifacts(app_name,stage_name)
        #Build CloudFormation template
        print('Building SAM Template')
        self.build_template(app_name,stage_name,bucket,zip_name,stage_settings)

    def publish_project(self,stage_name):
        for app_name in self.config.get('apps',[]):
            self.publish_app(app_name,stage_name)

    def upload_zip(self,zip_name,stage_settings):
        bucket = stage_settings.get('bucket')
        print('Uploading Zip {} to {} bucket.'.format(zip_name,bucket))
        s3.upload_file(zip_name,bucket,zip_name)
        return (bucket,zip_name)

    def get_env_vars(self,app_name,stage_name,stage_settings):
        return {'TEMPLATES_PATH':'/var/task/{}/templates'.format(app_name),
                'KEV_TEMPLATES_BUCKET':stage_settings.get('bucket')}

    def build_template(self,app_name,stage_name,bucket,zip_name,stage_settings):
        sam = sm.SAM(Description=self.config.get('description'), render_type='yaml')

        sam.add_parameter(sm.Parameter(name='Bucket', Type='String'))

        sam.add_parameter(sm.Parameter(name='CodeZipKey', Type='String'))

        app_stage = self.get_zip_name(app_name, stage_name, no_ext=True)


        sam.add_resource(sm.Function(
            name=app_name,
            CodeUri=sm.S3URI(
                Bucket=sm.Ref(Ref='Bucket'), Key=sm.Ref(Ref='CodeZipKey')),
            Handler='{app_name}.app.app'.format(app_name=app_name),
            Runtime='python3.6',
            Environment=sm.Environment(Variables=self.get_env_vars(app_name,stage_name,stage_settings)),
            Events=[sm.APIEvent(name=app_name, Path='{proxy+}', Method='get')]
        ))
        try:
            sam.publish(app_name,
                    Bucket=bucket,CodeZipKey=zip_name)
        except ChangeEmptyError:
            print('New Zip uploaded, CloudFormation template unchanged,')


    # def build_template(self,app_name,stage_name,s3_path):
    #     app_settings = self.get_app_config(app_name)
    #     lambda_settings = app_settings.get('resources').get('lambda')
    #     api_settings = app_settings.get('resources').get('api')
    #     sam = SAM()
    #     name = self.get_zip_name(app_name,stage_name,no_ext=True)
    #     if app_settings:
    #         sam.add_resource(
    #             API(name.replace('-',''),
    #                 StageName=name,
    #
    #                 )
    #         )
    #     if lambda_settings:
    #         #Add function
    #         sam.add_resource(
    #             Function(name.replace('-',''),
    #                      Handler=lambda_settings.get('handler'),
    #                      Runtime=lambda_settings.get('runtime'),
    #                      Description=lambda_settings.get('description', 'App deployed by Publish'),
    #                      MemorySize=lambda_settings.get('memory_size'),
    #                      Timeout=lambda_settings.get('timeout'),
    #                      Role=lambda_settings.get('role'),
    #                      Policies=lambda_settings.get('policies'),
    #
    #                      FunctionName=name,
    #                      CodeUri=s3_path)
    #         )
    #
    #     print('Publish to CloudFormation')
    #     sam.publish(name)
    #     print('Publish complete')

    def copy_app_files(self,app_name):

        shutil.copytree(app_name, '{}/{}'.format(
            self.get_virtualenv_path(app_name),app_name),
            ignore=shutil.ignore_patterns('app.yml', self.requirements_filename))

        with open('{}/{}/__init__.py'.format(
            self.get_virtualenv_path(app_name),app_name),'w+') as f:
            f.write('')

    def copy_capless(self,app_name):
        capless_path = '/home/brian/workspace/capless/capless'
        shutil.copytree(capless_path,'{}/capless'.format(self.get_virtualenv_path(app_name)))
        self.install_packages(app_name,'/home/brian/workspace/capless/requirements.txt')

    def install_packages(self,app_name,requirements_path):

        pip.main(['install','-r',
                  requirements_path,
                  '-t',self.get_virtualenv_path(app_name)])

    def build_zip(self, app_name, zip_name):
        shutil.make_archive(zip_name,'zip',self.get_virtualenv_path(app_name))

    def remove_build_artifacts(self,app_name,stage_name):
        shutil.rmtree(self.get_virtualenv_path(app_name))
        os.remove(self.get_zip_name(app_name,stage_name))

    def get_virtualenv_path(self,app_name):
        return '{}/{}'.format(app_name,self.venv)

    def get_zip_name(self,app_name,stage_name,no_ext=False):
        if no_ext:
            return '{}-{}'.format(app_name, stage_name)

        return '{}-{}.zip'.format(app_name, stage_name)

    def get_requirements_path(self,app_name):
        return '{}/{}'.format(app_name,self.requirements_filename)

    def get_app_config(self,name):
        return self.load_config('./{}/app.yml'.format(name))


