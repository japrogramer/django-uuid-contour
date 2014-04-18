#!/usr/bin/env python
from django.test.runner import DiscoverRunner
from django.conf import settings
import django

from optparse import OptionParser
import sys

# This is the package name, it is used in several places. If there are no args
# provided it sets the args to a set with pure_label in it
pure_label = 'uuid_contour'

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
            pure_label,
        ],
        ROOT_URLCONF='',
        DEBUG=False,
    )
    # settings are complete, this is run to ensure that the apps have been
    # setup
    django.setup()

def setup(test_labels):
    """
    For Django 1.7 apps are defined as having an apps.py and __init__.py.
    This function finds the tests submodule in the package and adds it to
    the INSTALLED_APPS setting but most importantly it loads the models for
    the test app so that there tables exist for the test
    """
    from django.apps import apps, AppConfig
    test_labels_set = set()
    for label in test_labels:
        test_labels_set.add('.'.join([pure_label, label]))

    module_label = list(label or module_label.startswith(label + '.')
            for label in test_labels_set)
    for module_name in module_label:
        settings.INSTALLED_APPS.append(module_name)
        app_config = AppConfig.create(module_name)
        apps.app_configs[app_config.label] = app_config
        app_config.import_models(apps.all_models[app_config.label])
        apps.clear_cache()

def runtests(verbosity, interactive, failfast, test_labels):
    # setup is run to find the tests submodule, this is joined with the
    # pure_label variable
    setup({'tests',})
    test_runner = DiscoverRunner( verbosity=verbosity,
            interactive=interactive,
            failfast=failfast,
            )
    # Finally run the tests and return the failures
    failures = test_runner.run_tests(test_labels)
    return failures

if __name__ == '__main__':
    # We add the acceptable options to the parser and sensible defaults
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

    # If no args are received test for the package labeled as dictated by
    # pure_label
    if not args:
        args = {pure_label,}

    failures = runtests(int(options.verbosity), options.interactive,
            options.failfast, args)

    if failures:
        sys.exit(failures)

