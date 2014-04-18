from django.db import models

from uuid_contour.fields import UUIDContour
import uuid

class UUIDPKContour(models.Model):
    uu = UUIDContour(immutable=True, primary_key=True)
    username = models.CharField(max_length=40)


class UUID1Contour(models.Model):
    username = models.CharField(max_length=40)
    uu = UUIDContour(standard=1)

    def __str__(self):
        return self.uu1.hex

class UUID3Contour(models.Model):
    username = models.CharField(max_length=40)
    uu = UUIDContour(standard=3,
            namespace=uuid.NAMESPACE_DNS,
            )

    def __str__(self):
        return self.uu3.hex

class UUID3ContourPlain(models.Model):
    username = models.CharField(max_length=40)
    uu = UUIDContour(standard=3)

    def __str__(self):
        return self.uu3.hex

class UUID4Contour(models.Model):
    username = models.CharField(max_length=40)
    uu = UUIDContour(immutable=True)

    def __str__(self):
        return self.uu4.hex

class UUID5Contour(models.Model):
    username = models.CharField(max_length=40)
    uu = UUIDContour(standard=5,
            namespace=uuid.NAMESPACE_DNS,
            )

    def __str__(self):
        return self.uu5.hex
