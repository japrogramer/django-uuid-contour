#!/usr/bin/env python
from django.test.runner import DiscoverRunner
from django.conf import settings

from optparse import OptionParser
import sys

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='django.db.backends.sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'uuid_contour_test',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sites',
            'django.contrib.messages',
            'uuid_contour',
            'uuid_contour.tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
    )


def runtests(verbosity, interactive, failfast, test_labels):
    test_runner = TestRunner( verbosity=verbosity,
            interactive=interactive,
            failfast=failfast,
            )
    failures = test_runner.run_tests(test_labels)
    return failures

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-v', '--verbosity', action='store', dest='verbosity',
            default='1', type='choice', choices=['0', '1', '2', '3'],
            help='Verbosity level; 0=minimal output, 1=normal output, 2=all '
                'output')
    parser.add_option('--failfast', action='store_true', dest='failfast',
            default=False,
            help='stop running the test suite after first failed test.')
    parser.add_option('--noinput', action='store_false', dest='interactive',
              default=True,
              help='do NOT prompt the user for input of any kind.')

    options, args = parser.parse_args()

    failures = runtests(int(options.verbosity), options.interactive,
            options.failfast, args)

    if failures:
        sys.exit(failurs)

