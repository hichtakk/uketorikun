from setuptools import setup
from codecs import open
import os
import re

version = ''
with open('uketorikun/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

requires = []
def _load_requires(path):
    return requires + [pkg.rstrip('\r\n') for pkg in open(path).readlines()]
    
setup(
    name='uketorikun',
    version=version,
    description='Slack bot for reading package label and registering addressee information to google sheets',
    long_description=long_description,
    url='https://github.com/hichtakk/uketorikun',
    author='hichtakk',
    author_email='hichtakk@gmail.com',
    license='apache',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='slack',
    install_requires=_load_requires('requirements.txt'),
    packages=['uketorikun'],
)
