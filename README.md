Django UUID Contour Field by japrogramer

General commands affected by apps.py
use label for ./manage migrate and other management commands other than test
    label = 'UUIDContour'
use name for running tests
    name = 'uuid_contour'

Use cases:
This package provides 4 variations of uuid, (1,3,4,5)
The Default is 4

the immutable option equall to True is equivalent of this options being set
    kwargs['unique'] = True
    kwargs['blank'] = True
    kwargs['editable'] = False

To use the uuid1 define a field in your model like this
from uuid_contour.fields import UUIDContour
class UUID1Contour(models.Model):
    username = models.CharField(max_length=40)
    uu = UUIDContour(standard=1)
To use it
    tt = uuid.uuid1([node[,clock_seq]])
    # The argument passed to the UUIDContour field can be either a uuid.UUID
    # or a str representation of a uuid with or without hyphens
    germane = UUID3Contour._default_manager.create(username='something', uu=tt)

You can use bytes to define a UUIDContour
    tt = b'\x81[\xb5~\xbc\xa9G6\x80WvIU\x92\xbc\x1e'
    germane = UUID1Contour._default_manager.create(username='uuid4',
                uu=tt
                )
This standard can also take two additional arguments related to uuid1
    uu = UUIDContour(standard=1, node=None, clock_seq=None)

To use the uuid3,5 provide standard 3 or 5
class UUID5Contour(models.Model):
    username = models.CharField(max_length=40)
    uu = UUIDContour(standard=5)

To use it
    username = 'some value'
    tt = uuid.uuid5(uuid.NAMESPACE_DNS, username)
    germane = UUID1Contour._default_manager.create(username=username,
                uu=tt
                )

To filter by a uuid, you can use a uuid.UUID instance or string version of the
uuid with or without hyphens
class UUID4Contour(models.Model):
    username = models.CharField(max_length=40)
    uu = UUIDContour(immutable=True)

And to query by a uuid
    tt = uuid.uuid4()
    o_uuid = tt.hex
    pertinent = UUID4Contour._default_manager.get(uu__exact=o_uuid)

Verifying uuids: if you are allowing a user to set a uuid field, uuid contour
    provides to regex to match hypenated and unhyohenated uuid str they are ph
    and pu respectively, they can be crafted into your forms validation
