from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from uuid_contour.tests.models import (UUID1Contour, UUID3Contour,
        UUID4Contour, UUID5Contour)
from uuid_contour.fields import ph, pu
import uuid

class UUIDContour(TestCase):
