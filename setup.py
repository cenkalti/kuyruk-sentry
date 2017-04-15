# coding=utf8
from setuptools import setup

setup(
    name='Kuyruk-Sentry',
    version="1.1.3",
    author=u'Cenk Altı',
    author_email='cenkalti@gmail.com',
    keywords='kuyruk sentry',
    url='https://github.com/cenkalti/kuyruk-sentry',
    py_modules=["kuyruk_sentry"],
    install_requires=[
        'kuyruk>=8.0.0',
        'raven>=5.1.1',
    ],
    entry_points={'kuyruk.config': 'sentry = kuyruk_sentry:CONFIG'},
    description='Sends exceptions in Kuyruk workers to Sentry.',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Object Brokering',
        'Topic :: System :: Distributed Computing',
    ],
)
