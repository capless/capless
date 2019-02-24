import click

from capless.utils.config import load_config


def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

MEMORY_CHOICES = [str(i) for i in drange(128,3072,64)]

REGION_CHOICES = ['us-east-1', 'us-east-2','us-west-1','us-west-2',
                  'ca-central-1','eu-west-1','eu-central-1','eu-west-2',
                  'ap-southeast-1','ap-southeast-2','ap-northeast-1',
                  'ap-northeast-2','ap-south-1','sa-east-1']


@click.group()
def capless():
    pass


@capless.command()
@click.option('--project-name',prompt=True,)
@click.option('--description',prompt=True)
@click.option('--bucket',prompt=True)
@click.option('--memory',prompt=True,type=click.Choice(MEMORY_CHOICES))
@click.option('--cache-cluster',prompt=True,type=click.Choice(['True','False']))
@click.option('--region',prompt=True,type=click.Choice(REGION_CHOICES))
def init(project_name,description,bucket,memory,cache_cluster,region):
    pass


def local():
    pass


def create_project():
    pass


def deploy():
    pass


def undeploy():
    pass


def generate_swagger():
    config = load_config()

