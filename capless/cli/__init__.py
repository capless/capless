import os

import click
import boto3

from ..publish.client import Publish
from ..core.exceptions import CappyInitializeError
from .helper import CaplessCLI

s3 = boto3.client('s3')

@click.group()
def capless():
    pass

def check_for_project_config_app(ctx, param, value):
    if not os.path.isfile('capless.yaml'):
        click.echo(click.style('There is no capless.yaml in your '
            'current directory. Capless will assume you are creating an '
            'app outside of a project',fg='yellow'))
        ctx.abort()
    if os.path.isdir(value):
        click.echo(click.style('There is already an app named {} '
                               'in this project.'.format(value),fg='yellow'))
        ctx.abort()
    return value

def check_for_project_config_project(ctx,param,value):
    if os.path.isfile('capless.yaml'):
        click.echo(click.style('There is already capless.yaml in your '
                               'current directory. Please run this command again after '
                               'switching to a directory without a capless.yaml', fg='red'))
        ctx.abort()
    return value

def list_buckets():
    return [i.get('Name') for i in s3.list_buckets().get('Buckets')]

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
@click.option('--description',prompt=True)
@click.option('--default-stage',default='dev',prompt=True)
@click.option('--region',default='us-east-1',prompt=True,type=click.Choice(
    ['us-east-1', 'us-east-2','us-west-1','us-west-2','ca-central-1',
     'eu-west-1','eu-central-1','eu-west-2','ap-southeast-1','ap-southeast-2',
     'ap-northeast-1','ap-northeast-2','ap-south-1','sa-east-1'
     ]))
@click.option('--bucket',prompt=True,
              type=click.Choice(list_buckets()),
              help='Make sure that these S3 buckets are already created and '
                   'that you list a bucket for every region you have specified')
@click.option('--use-cloudfront', is_flag=True,prompt=True)
def create_project(name,description,bucket,default_stage,region,use_cloudfront,**kwargs):
    options = {
        'name': name,
        'description':description,
        'stages':{
            default_stage:{
                'bucket':bucket,
                'region': region,
                'use_cloudfront': use_cloudfront
            }
        },
        'apps':[]
    }
    if kwargs:
        options.update(kwargs)
    CaplessCLI().create_project(options)

@capless.command()
@click.option('--name',prompt=True,callback=check_for_project_config_app)
@click.option('--description',prompt=True)
def create_app(name,description,**kwargs):
    options = {
        'name':name,
        'description':description,
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

@capless.command()
@click.argument('app_name')
@click.argument('stage')
def publish_app(app_name,stage):
    p = Publish()
    p.publish_app(app_name,stage)

if __name__ == '__main__':
    capless()