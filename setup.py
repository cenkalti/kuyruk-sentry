# coding=utf8
from setuptools import setup

setup(
    name='Kuyruk-Sentry',
    version="1.1.1",
    author=u'Cenk Altı',
    author_email='cenkalti@gmail.com',
    keywords='kuyruk sentry',
    url='https://github.com/cenkalti/kuyruk-sentry',
    py_modules=["kuyruk_sentry"],
    install_requires=[
        'kuyruk>=6.0.0',
        'raven>=5.1.1',
    ],
    entry_points={'kuyruk.config': 'sentry = kuyruk_sentry:CONFIG'},
    description='Sends exceptions in Kuyruk workers to Sentry.',
    long_description=open('README.md').read(),
)
