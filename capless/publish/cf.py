import sys
import yaml
from troposphere import Template, Join, Ref
from troposphere.cloudfront import (Distribution, DistributionConfig,
                                    Origin, CustomOrigin, DefaultCacheBehavior,
                                    ForwardedValues, Cookies, S3Origin, CacheBehavior)


class CloudFront(object):
    config_path = 'app.yml'

    def __init__(self, config=None, config_path=None):
        self.load_config(config,config_path)
        self.cf_config = self.config.get('cloudfront', None)
        if self.cf_config:
            self.distribution_name = self.cf_config.keys()[0]
        self.t = Template()
        self.create_distribution()

    def load_config(self,config,config_path=None):
        if config:
            self.config = config
            return
        config_filename = config_path or self.config_path
        try:
            with open(config_filename, 'r') as f:
                self.config = yaml.safe_load(f)
        except IOError:
            self.config = dict()

    def create_distribution(self):
        origins, behaviours = self._construct_origins()
        self.t.add_resource(Distribution(
            self.distribution_name,
            DistributionConfig=DistributionConfig(
                Origins=origins,
                CacheBehaviors=behaviours,
                DefaultCacheBehavior=DefaultCacheBehavior(
                    AllowedMethods=['GET', 'HEAD'],
                    CachedMethods=['GET', 'HEAD'],
                    ForwardedValues=ForwardedValues(
                        QueryString=True,
                        Headers=[],
                        Cookies=Cookies(Forward='none')
                    ),
                    TargetOriginId=origins[0].Id,
                    ViewerProtocolPolicy='https-only'
                ),
                Enabled = True
            )
        ))

    def _construct_origins(self):
        origins = []
        behaviors = []
        origin_ids = self.cf_config[self.distribution_name].keys()
        for origin_id in origin_ids:
            kwargs = self.cf_config[self.distribution_name][origin_id].copy()
            CloudFront.capitalize_keys(kwargs)
            CloudFront._prepare_origins(kwargs)
            CloudFront._prepare_behaviors(kwargs)
            kwargs['Origin']['Id'] = origin_id
            origins.append(Origin(**kwargs['Origin']))
            kwargs['Behaviors']['TargetOriginId'] = origin_id
            behaviors.append(CacheBehavior(**kwargs['Behaviors']))
        return origins, behaviors

    @staticmethod
    def capitalize(string):
        return ''.join([x.capitalize() for x in string.split('_')])

    @staticmethod
    def capitalize_keys(dictionary):
        if isinstance(dictionary, dict):
            for key in dictionary.keys():
                capitalized_key = CloudFront.capitalize(key)
                value = dictionary.pop(key)
                dictionary[capitalized_key] = value
                if isinstance(value, dict):
                    CloudFront.capitalize_keys(dictionary[capitalized_key])

    @staticmethod
    def _prepare_behaviors(dictionary):
        behaviors = dictionary['Behaviors']
        key = 'ForwardedValues'
        if key in behaviors:
            if 'Cookies' in behaviors[key]:
                behaviors[key]['Cookies'] = \
                    getattr(sys.modules[__name__], 'Cookies')(**behaviors[key]['Cookies'])
            behaviors[key] = getattr(sys.modules[__name__], key)(**behaviors[key])

    @staticmethod
    def _prepare_origins(dictionary):
        class_name_replace = {'S3OriginConfig': 'S3Origin',
                              'CustomOriginConfig': 'CustomOrigin'}
        custom_origin_replace = {'HttpPort': 'HTTPPort',
                                 'HttpsPort': 'HTTPSPort'}
        origin = dictionary['Origin']
        # for these keys a value should be a corresponding class instance
        for key in ['CustomOriginConfig', 'S3OriginConfig','OriginCustomHeaders']:
            if key in origin:
                # need to rename HttpPort-> HTTPPort, HttpsPort-> HTTPSPort
                if key is 'CustomOriginConfig':
                    for custom_origin_key in origin[key].keys():
                        origin[key][custom_origin_replace.get(
                            custom_origin_key, custom_origin_key)] =\
                            origin[key].pop(custom_origin_key)
                origin[key] = getattr(sys.modules[__name__],
                                      class_name_replace.get(key, key))(**origin[key])

    def to_json(self):
        return self.t.to_json()

    def to_dict(self):
        return self.t.to_dict()
