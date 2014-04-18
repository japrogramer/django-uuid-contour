Django UUID Contour Field by japrogramer

General commands affected by apps.py
use label for ./manage migrate and other management commands other than test
    label = 'UUIDContour'
use name for running tests
    name = 'uuid_contour'

Use cases:
This package provides 4 variations of uuid, (1,3,4,5)

To use the uuid1 define a field in your model like this
class UUID1Contour(models.Model):
    username = models.CharField(max_length=40)
    uu = UUIDContour(standard=1)
To use it
    tt = uuid.uuid1([node[,clock_seq]])
    # The argument passed to the UUIDContour field can be either a uuid.UUID
    # or a str representation of a uuid with or without hyphens
    germane = UUID3Contour._default_manager.create(username='something', uu=tt)
This standard can also take two additional arguments related to uuid1
    uu = UUIDContour(standard=1, node=None, clock_seq=None)

To use the uuid3,5 provide standard 3 or 5
    tt = uuid.uuid3(uuid.NAMESPACE_DNS, 'uuid3')


