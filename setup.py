from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='analyzer',
    version='1.0.1',
    description='GitHub repository analyzer',
    license='MIT',
    url='https://github.com/63phc/analyzer',
    author='63phc',
    author_email='pavel.burns@gmail.com',
    packages=find_packages('analyzer'),
    package_dir={'': 'analyzer'},
    project_urls={
        'Bug Reports': 'https://github.com/63phc/analyzer/issues',
    }
)
