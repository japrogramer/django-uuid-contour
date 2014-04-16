from django.apps import AppConfig
from django.conf import settings

class BaseConfig(AppConfig):
    name = 'uuid_contour.tests'
    label = 'UUIDContourTests'
    verbosename = 'Test uuid Field'

DefaultConfig = BaseConfig

