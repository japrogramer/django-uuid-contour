from django.db import models
from django.utils.translation import ugettext as _

class UUIDContour(models.Field, metaclass=models.SubfieldBase):
    description = _('uuid(%(standard)s) max_length is %(max_length)s')

    def __init__(self, standard, *args, **kwargs):
        kwargs['max_length'] = 36
        super(UUIDContour, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return None
        return super

    def formfield(self):
        canonical = {
            'form_class': forms.CharField,
            'max_length': self.max_length,
        }
        defaults.update(kwargs)
        return super(UUIDContour, self).formfield(**canonical)

    def deconstruct(self):
        name, path, args, kwargs = super(UUIDContour, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs
