from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from uuid_contour.tests.models import (UUID1Contour, UUID3Contour,
        UUID4Contour, UUID5Contour)
from uuid_contour.fields import ph, pu
import uuid

class UUIDContour(TestCase):

    def test_uuid1_returns_hex(self):
        relevant_model = UUID1Contour._default_manager.create(username='uuid1')

    def test_uuid4_returns_hex(self):
        relevant_model = UUID4Contour._default_manager.create(username='uuid4')
        print(relevant_model.uu4.hex)
        self.assertTrue(relevant_model.uu4.hex)
