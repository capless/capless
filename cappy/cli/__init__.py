import click
import yaml
from .cli import CappyCLI

@click.group()
def cappy():
    pass

def use_apigw(ctx, param, value):
    """
    Callback for use-api-gateway option in the create_project command. Adds the
    answers to follow-up questions to the context dict
    :param ctx: Context
    :param param: Parameter
    :param value: Value retrieved from the prompt
    :return:
    """
    if not value or ctx.resilient_parsing:
        return
    ctx.params['region'] = click.prompt('API Gateway Region',default='us-east-1',
                          show_default=True)
    ctx.params['use_cloudfront'] = click.prompt('Use CloudFront? [y/N]',type=bool)

def use_apigw_app(ctx, param, value):
    """
    Callback for use-api-gateway option in the create_app command. Adds the
    answers to follow-up questions to the context dict
    :param ctx: Context
    :param param: Parameter
    :param value: Value retrieved from the prompt
    :return:
    """
    if not value or ctx.resilient_parsing:
        return
    ctx.params['default_apigw_resource'] = click.prompt('Default API Gateway Resource',default=None,
                                 show_default=True)

@cappy.command()
@click.option('--name',prompt=True)
@click.option('--default-stage',default='dev',prompt=True)
@click.option('--auto-admin-prefix',is_flag=True,prompt=True,expose_value=True)
@click.option('--use-api-gateway', is_flag=True,prompt=True,expose_value=False,
              callback=use_apigw)
def create_project(name,default_stage,**kwargs):

    options = {
        'name': name,
        'default_stage': default_stage,
    }
    if kwargs:
        options.update(kwargs)
    CappyCLI().create_project(options)

@cappy.command()
@click.option('--name',prompt=True)
@click.option('--use-api-gateway',prompt=True,is_flag=True,
              callback=use_apigw_app,expose_value=False)
def create_app(name,**kwargs):
    options = {
        'name':name,
    }
    if kwargs:
        options.update(kwargs)
    CappyCLI().create_app(options)

@cappy.command()
@click.option('--name',prompt=True)
def create_function(name,**kwargs):
    options = {
        'name':name
    }
    if kwargs:
        options.update(kwargs)
    CappyCLI().create_function()

if __name__ == '__main__':
    cappy()