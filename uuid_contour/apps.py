from django.apps import AppConfig
from django.conf import settings

class BaseConfig(AppConfig):
    name = 'uuid_contour'
    label = 'UUIDContour'
    verbosename = 'A uuid Field'

DefaultConfig = BaseConfig

