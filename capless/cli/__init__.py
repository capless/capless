import os

import click

from ..core.exceptions import CappyInitializeError
from .helper import CaplessCLI

@click.group()
def capless():
    pass

def check_for_project_config_app(ctx, param, value):
    if not os.path.isfile('capless.yaml'):
        click.echo(click.style('There is no capless.yaml in your '
            'current directory. Capless will assume you are creating an '
            'app outside of a project',fg='yellow'))
    return value

def check_for_project_config_project(ctx,param,value):
    if os.path.isfile('capless.yaml'):
        click.echo(click.style('There is already capless.yaml in your '
                               'current directory. Please run this command again after '
                               'switching to a directory without a capless.yaml', fg='red'))
        ctx.abort()
    return value

def event_source_type_cb(ctx, param, value):
    choices = ('apigw', 's3', 'sns', 'cloudwatch', 'rds', 'dyndb')
    if value not in choices:
        click.echo(click.style(
            'Event source type should be one of the following: {}. Value given: {}'.format(
                ', '.join(choices),value),fg='red'))
        ctx.abort()
    return value

@capless.command()
@click.option('--name',prompt=True,callback=check_for_project_config_project)
@click.option('--default-stage',default='dev',prompt=True)
@click.option('--regions',default='us-east-1,us-east-2',
              help='Regions that this application should be deployed. Comma delimted.',
              prompt=True)
@click.option('--use-cloudfront', is_flag=True,prompt=True)
def create_project(name,default_stage,regions,use_cloudfront,**kwargs):
    split_regions = regions.split(',')
    options = {
        'name': name,
        'regions':split_regions,
        'use_cloudfront':use_cloudfront,
        'default_stage': default_stage,
        'apps':[]
    }
    if kwargs:
        options.update(kwargs)
    CaplessCLI().create_project(options)

@capless.command()
@click.option('--name',prompt=True,callback=check_for_project_config_app)
def create_app(name,**kwargs):
    options = {
        'name':name,
        'functions':[],
    }
    if kwargs:
        options.update(kwargs)
    CaplessCLI().create_app(options)

@capless.command()
@click.option('--name',prompt=True)
@click.option('--event-source-type',prompt=True,default='apigw',
              help='Valid choices are apigw, s3, sns, cloudwatch, rds, dyndb',
              callback=event_source_type_cb)
def create_function(name,event_source_type,**kwargs):
    options = {
        'name':name,
        'event_source_type':event_source_type
    }
    if kwargs:
        options.update(kwargs)
    cap = CaplessCLI()
    try:
        cap.update_config('app.yaml', 'functions', options,file_required=True)
    except CappyInitializeError as m:
        click.echo(click.style(str(m),fg='red'))
        raise click.Abort()
    cap.create_function(options)

if __name__ == '__main__':
    capless()