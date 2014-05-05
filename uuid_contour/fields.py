from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import uuid
import re

# uuids, xxxxxxxx-xxxx-Mxxx-Nxxx-xxxxxxxxxxxx where M is the
# version and N is the variant
ph = re.compile(r'[a-f0-9]{8}-[a-f0-9]{4}-(?P<version>[1-5])[a-f0-9]{3}'
        r'-(?P<variant>[89ab])[a-f0-9]{3}-[a-f0-9]{12}')
pu = re.compile(r'[a-f0-9]{8}[a-f0-9]{4}(?P<version>[1-5])[a-f0-9]{3}'
        r'(?P<variant>[89ab])[a-f0-9]{3}[a-f0-9]{12}')

class UUIDContour(models.Field, metaclass=models.SubfieldBase):
    description = _('uuid(%(standard)s) max_length is %(max_length)s')

    def __init__(self, standard=4, immutable=False, name=None,
            namespace=None, node=None, clock_seq=None, *args, **kwargs):
        if standard not in (1, 3, 4, 5):
            raise ValueError('%s  is not available' % standard)
        self.standard = standard
        self.immutable = immutable
        if immutable:
            kwargs['unique'] = True
            kwargs['blank'] = True
            kwargs['editable'] = False
        self.node, self.clock_seq = node, clock_seq
        self.namespace, self.name = namespace, name
        kwargs['max_length'] = 32
        super(UUIDContour, self).__init__(*args, **kwargs)

    def _generate_uuid(self):
        if self.standard is 1:
            uuid_kwargs = {'node': self.node, 'clock_seq': self.clock_seq,}
        if self.standard in (3, 5):
            errors = {
                    'error': False,
                    'namespace': '',
                    'name': '',
                    }
            if self.namespace is None:
                errors['error'] = True
                errors['namespace'] =  ' namespace'
            if self.name is None:
                errors['error'] = True
                errors['name'] =  ' name'
            if errors['error']:
                raise ValidationError(_('missing:%(namespace)s%(name)s'),
                        code='missing params',
                        params=errors)
            uuid_kwargs = {'name': self.name, 'namespace': self.namespace,}
        else:
            uuid_kwargs = {}
        return getattr(uuid, 'uuid%s' % self.standard)(*uuid_kwargs)

    def db_type(self, connection):
        if (connection.settings_dict['ENGINE'] ==
                'django.db.backends.postgresql_psycopg2'):
            return 'uuid'
        return 'char(%s)' % self.max_length

    def get_db_prep_value(self, value, connection, prepared=False):
        # If the value has been prepared than it is suitable to be used with
        # the db
        if prepared:
            return value
        else:
            value = super(UUIDContour, self).get_db_prep_value(
                    value, connection)
        return value

    def get_prep_value(self, value):
        # prepare for use in a query
        if isinstance(value, uuid.UUID):
            return value.hex
        if isinstance(value, str):
            if '-' in value:
                return value.replace('-', '')
        return value

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if not value and add:
            value = self._generate_uuid()
            setattr(model_instance, self.attname, value)
            return value.hex
        return value

    def to_python(self, value):
        # value returned by the database or serializer, return a uuid.UUID
        if not value:
            return None
        if isinstance(value, uuid.UUID):
            return value
        elif isinstance(value, type(b'')):
            return uuid.UUID(bytes=value)
        try:
            value = uuid.UUID(value)
        except ValueError as e:
            raise ValidationError(_('Invalid Value: %(value)s: %(msg)s'),
                    code='failed uuid',
                    params={
                        'value': value,
                        'msg': str(e),
                        })
        return value

    def value_to_string(self, obj):
         value = self._get_val_from_obj(obj)
         return self.get_prep_value(value)

    def formfield(self, **kwargs):
        canonical = {
            'form_class': forms.CharField,
            'max_length': self.max_length,
        }
        canonical.update(kwargs)
        return super(UUIDContour, self).formfield(**canonical)

    def deconstruct(self):
        name, path, args, kwargs = super(UUIDContour, self).deconstruct()
        del kwargs['max_length']
        if self.immutable:
            kwargs['unique'] = True
            kwargs['blank'] = True
            kwargs['editable'] = False
        if self.node is not None and self.clock_seq is not None:
            kwargs['node'] = self.node
            kwargs['clock_seq'] = self.clock_seq
        if self.name is not None and self.namespace is not None:
            kwargs['name'] = self.name
            kwargs['namespace'] = self.namespace
        return name, path, args, kwargs
