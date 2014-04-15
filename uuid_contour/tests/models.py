from django.db import models

from uuid_contour import UUIDContour
import uuid

class UUID1Contour(UUIDContour):
    username = models.CharField(max_length=40)
    uu1 = UUIDContour(standard=1)

    def __str__(self):
        return self.uu1.hex

class UUID3Contour(UUIDContour):
    username = models.CharField(max_length=40)
    uu3 = UUIDContour(standard=3,
            namespace=uuid.NAMESPACE_DNS,
            name=self.username)

    def __str__(self):
        return self.uu3.hex

class UUID4Contour(UUIDContour):
    username = models.CharField(max_length=40)
    uu4 = UUIDContour(immutable=True)

    def __str__(self):
        return self.uu4.hex

class UUID5Contour(UUIDContour):
    username = models.CharField(max_length=40)
    uu5 = UUIDContour(standard=5,
            namespace=uuid.NAMESPACE_DNS,
            name=self.username)

    def __str__(self):
        return self.uu5.hex
