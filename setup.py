from setuptools import setup, find_packages

from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)

setup(
    name='capless',
    description='Python Serverless Framework',
    url='https://github.com/capless/capless',
    author='Brian Jinwright',
    license='GNU GPL v3',
    keywords='serverless, framework,',
    install_requires=[str(ir.req) for ir in install_reqs],
    packages=find_packages(),
    version='0.1.0',
    entry_points='''
        [console_scripts]
        capless=capless.cli:capless
        ''',
)