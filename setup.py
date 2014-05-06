import os
from setuptools import setup, find_packages

CURRENT_DIR = os.path.dirname(__file__)
def read(fname):
    return open(os.path.join(CURRENT_DIR, fname)).read()

# Info for setup
PACKAGE = 'uuid_contour'
NAME = 'django-uuid-contour'
DESCRIPTION = 'A Django app for uuid fields'
AUTHOR = 'Jorge Perez'
AUTHOR_EMAIL = 'japrogramer@gmail.com'
URL = 'https://github.com/japrogramer/django-uuid-contour'
VERSION = __import__(PACKAGE).__version__

# setup call
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read('README.md'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='BSD',
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
         'Development Status :: 4 - Beta',
         'Environment :: Web Environment',
         'Intended Audience :: Developers',
         'License :: OSI Approved :: BSD License',
         'Operating System :: OS Independent',
         'Programming Language :: Python :: 3',
         'Framework :: Django',
    ],
    install_requires=[
         'django>=1.7b1',
    ],
    zip_safe=False,
    )
