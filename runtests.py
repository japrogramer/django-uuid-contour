#!/usr/bin/env python
from django.test.runner import DiscoverRunner
from django.conf import settings
import django

from optparse import OptionParser
import sys

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
    # settings are complete
    django.setup()

def setup(test_labels):
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
    setup({'tests',})
    test_runner = DiscoverRunner( verbosity=verbosity,
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

    if not args:
        args = {pure_label,}

    failures = runtests(int(options.verbosity), options.interactive,
            options.failfast, args)

    if failures:
        sys.exit(failures)

