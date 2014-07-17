#!/usr/bin/env python
from django.apps import apps, AppConfig
from django.test.utils import get_runner
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils._os import upath
import django

from argparse import ArgumentParser
import sys
import os
import tempfile
import logging
import shutil

from celery import Celery

# This is the package name, it is used in several places. If there are no args
# provided it sets the args to a set with pure_label in it

TEST_TEMPLATE_DIR = 'test_templates'

RUNTESTS_DIR = os.path.abspath(os.path.dirname(upath(__file__)))
TEMP_DIR = tempfile.mkdtemp(prefix='django_')
os.environ['DJANGO_TEST_TEMP_DIR'] = TEMP_DIR

ALWAYS_INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.staticfiles',
]

ALWAYS_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='django.db.backends.sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'uuid_contour_test',
            }
        },
        DEBUG=False,
        # for login required decorator
        #LOGIN_URL = reverse_lazy('denyzen:signin'),
        #DENYZEN_SIGNIN_REDIRECT_URL = 'admin:login',
        # Email
        #EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend',
        #DEFAULT_FROM_EMAIL = 'My Domain <noreply@mydomain.com>',
        # Celery
        #BROKER_URL = 'redis://localhost:6379/0',
        #CELERY_RESULT_BACKEND = 'redis://localhost:6379/1',
        #CELERY_ALWAYS_EAGER = True,
        #CELERY_EAGER_PROPAGATES_EXCEPTIONS = True,
    )

    # set the default Django settings module for the 'celery' program.
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sandbox.settings')
    #celery_app = Celery('sandbox')

    #celery_app.config_from_object('django.conf:settings')
    #celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

def get_test_modules():
    modules = []
    discovery_paths = [
        (None, RUNTESTS_DIR),
    ]

    for modpath, dirpath in discovery_paths:
        for f in os.listdir(dirpath):
            if ('.' in f or
                    os.path.isfile(f) or
                    not os.path.exists(os.path.join(dirpath, f, '__init__.py'))):
                continue
            modules.append((modpath, f))
            modules.append((f, 'tests'))
    return modules

def get_installed():
    return [app_config.name for app_config in apps.get_app_configs()]

def setup(verbosity, test_labels):
    state = {
        'INSTALLED_APPS': settings.INSTALLED_APPS,
        'ROOT_URLCONF': getattr(settings, "ROOT_URLCONF", ""),
        'TEMPLATE_DIRS': settings.TEMPLATE_DIRS,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'STATIC_URL': settings.STATIC_URL,
        'STATIC_ROOT': settings.STATIC_ROOT,
        'MIDDLEWARE_CLASSES': settings.MIDDLEWARE_CLASSES,
    }

    settings.INSTALLED_APPS = ALWAYS_INSTALLED_APPS
    settings.ROOT_URLCONF = 'denyzen.tests.urls'
    settings.STATIC_URL = '/static/'
    settings.STATIC_ROOT = os.path.join(TEMP_DIR, 'static')
    settings.TEMPLATE_DIRS = (os.path.join(RUNTESTS_DIR, TEST_TEMPLATE_DIR),)
    settings.LANGUAGE_CODE = 'en'
    settings.SITE_ID = 1
    settings.MIDDLEWARE_CLASSES = ALWAYS_MIDDLEWARE_CLASSES
    # Ensure the middleware classes are seen as overridden otherwise we get a compatibility warning.
    #settings._explicit_settings.add('MIDDLEWARE_CLASSES')
    settings.MIGRATION_MODULES = {
        # these 'tests.migrations' modules don't actually exist, but this lets
        # us skip creating migrations for the test models.
        'auth': 'django.contrib.auth.tests.migrations',
        'contenttypes': 'django.contrib.contenttypes.tests.migrations',
    }

    # Load all the ALWAYS_INSTALLED_APPS.
    django.setup()

    if verbosity > 0:
        # Ensure any warnings captured to logging are piped through a verbose
        # logging handler.  If any -W options were passed explicitly on command
        # line, warnings are not captured, and this has no effect.
        logger = logging.getLogger('py.warnings')
        handler = logging.StreamHandler()
        logger.addHandler(handler)

    # Load all the test model apps.
    test_modules = get_test_modules()
    print(test_modules)

    test_labels_set = set()
    for label in test_labels:
        test_labels_set.add(label)

    installed_app_names = set(get_installed())
    for modpath, module_name in test_modules:
        if modpath:
            module_label = '.'.join([modpath, module_name])
        else:
            module_label = module_name
        # if the module (or an ancestor) was named on the command line, or
        # no modules were named (i.e., run all), import
        # this module and add it to INSTALLED_APPS.
        if not test_labels:
            module_found_in_labels = True
        else:
            module_found_in_labels = any(
                # exact match or ancestor match
                module_label == label or module_label.startswith(label + '.')
                for label in test_labels_set)

        if module_found_in_labels and module_label not in installed_app_names:
            if verbosity >= 2:
                print("Importing application %s" % module_name)
            settings.INSTALLED_APPS.append(module_label)
            app_config = AppConfig.create(module_name)
            apps.app_configs[app_config.label] = app_config
            app_config.import_models(apps.all_models[app_config.label])
            apps.clear_cache()

    apps.set_installed_apps(settings.INSTALLED_APPS)

    return state

def teardown(state):
    try:
        # Removing the temporary TEMP_DIR. Ensure we pass in unicode
        # so that it will successfully remove temp trees containing
        # non-ASCII filenames on Windows. (We're assuming the temp dir
        # name itself does not contain non-ASCII characters.)
        shutil.rmtree(TEMP_DIR)
    except OSError:
        print('Failed to remove temp directory: %s' % TEMP_DIR)

    # Restore the old settings.
    for key, value in state.items():
        setattr(settings, key, value)

def runtests(verbosity, interactive, failfast, test_labels):
    # setup is run to find the tests submodule, this is joined with the
    # pure_label variable
    state = setup(verbosity, test_labels)
    extra_tests = []

    if not hasattr(settings, 'TEST_RUNNER'):
        settings.TEST_RUNNER = 'django.test.runner.DiscoverRunner'
    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        verbosity=verbosity,
        interactive=interactive,
        failfast=failfast,
    )
    # Finally run the tests and return the failures
    failures = test_runner.run_tests(
        test_labels, extra_tests=extra_tests)

    teardown(state)
    return failures

if __name__ == '__main__':
    # We add the acceptable options to the parser and sensible defaults
    parser = ArgumentParser(description="Run the Django test suite.")
    parser.add_argument('modules', nargs='*', metavar='module',
        help='Optional path(s) to test modules;')
    parser.add_argument(
        '-v', '--verbosity', default=1, type=int, choices=[0, 1, 2, 3],
        help='Verbosity level; 0=minimal output, 1=normal output, 2=all output')
    parser.add_argument(
        '--noinput', action='store_false', dest='interactive', default=True,
        help='Tells Django to NOT prompt the user for input of any kind.')
    parser.add_argument(
        '--failfast', action='store_true', dest='failfast', default=False,
        help='Tells Django to stop running the test suite after first failed '
             'test.')
    parser.add_argument(
        '--settings',
        help='Python path to settings module, e.g. "myproject.settings". If '
             'this isn\'t provided, either the DJANGO_SETTINGS_MODULE '
             'environment variable or "test_sqlite" will be used.')

    options = parser.parse_args()

    # Allow including a trailing slash on app_labels for tab completion convenience
    options.modules = [os.path.normpath(labels) for labels in options.modules]

    if options.settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
    else:
        if "DJANGO_SETTINGS_MODULE" not in os.environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = 'sandbox.settings'
        options.settings = os.environ['DJANGO_SETTINGS_MODULE']

    failures = runtests(options.verbosity, options.interactive,
                            options.failfast, options.modules)

    if failures:
        sys.exit(bool(failures))

