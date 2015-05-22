import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


config = {
    'name': 'minimail',
    'description': 'A teeny tiny mail sender',
    'author': 'Cooper Stimson',
    'author_email': 'cooper@cooperstimson.com',
    'url': 'github.com/6c1/minimail',
    'version': '0.1',
    'packages': ['minimail'],
    'license': 'MIT',
    'long_description': read('README.md'),
    'classifiers': ['Development Status :: 3 - Alpha',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Programming Language :: Python :: 2.7',
                    'License :: OSI Approved :: MIT License',
                    'Topic :: Communications :: Email']
}


setup(**config)
