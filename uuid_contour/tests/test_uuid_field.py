from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from uuid_contour.tests.models import (UUID1Contour, UUID3Contour,
        UUID4Contour, UUID5Contour, UUIDPKContour)
from uuid_contour.fields import ph, pu
import uuid

class UUIDContour(TestCase):

    def test_uuid_as_pk(self):
        germane = UUIDPKContour._default_manager.create(username='uuidpk')
        pertinent = UUIDPKContour._default_manager.get(pk=germane.pk)
        self.assertTrue(isinstance(germane.pk, uuid.UUID))
        self.assertEqual(germane, pertinent)

    def test_uuid1_returns_hex(self):
        germane = UUID1Contour._default_manager.create(username='uuid1')
        self.assertTrue(isinstance(germane.uu, uuid.UUID))

    def test_uuid_get_returns_same_uuid(self):
        germane = UUID1Contour._default_manager.create(username='uuid1')
        o_uuid = germane.uu.hex
        pertinent = UUID1Contour._default_manager.get(uu__exact=o_uuid)
        self.assertEqual(o_uuid, pertinent.uu.hex)

    def test_uuid3_returns_hex(self):
        tt = uuid.uuid3(uuid.NAMESPACE_DNS, 'uuid3')
        germane = UUID3Contour._default_manager.create(username='uuid3',
                uu=tt)
        self.assertTrue(isinstance(germane.uu, uuid.UUID))
        self.assertEqual(germane.uu, tt)

    def test_uuid4_returns_hex(self):
        germane = UUID4Contour._default_manager.create(username='uuid4')
        self.assertTrue(germane.uu.hex)

    def test_uuid5_returns_hex(self):
        tt = uuid.uuid5(uuid.NAMESPACE_DNS, 'uuid5')
        germane = UUID5Contour._default_manager.create(username='uuid5',
                uu=tt)
        self.assertTrue(isinstance(germane.uu, uuid.UUID))
        self.assertEqual(germane.uu, tt)
