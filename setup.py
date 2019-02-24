from setuptools import setup, find_packages

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


VERSION = '0.1.0'

setup(
    name='capless',
    description='Python Serverless Framework',
    url='https://github.com/capless/capless',
    author='Brian Jinwright',
    license='GNU GPL v3',
    keywords='serverless, framework,',
    install_requires=parse_requirements('requirements.txt'),
    packages=find_packages(),
    version=VERSION,
    entry_points='''
        [console_scripts]
        capless=capless.cli:capless
        ''',
)
