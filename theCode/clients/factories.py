import factory
from factory import LazyAttribute, DjangoModelFactory

from models import UserModel


class UserModelFactory(DjangoModelFactory):
    class Meta:
        model = 'clients.UserModel'
    #    django_get_or_create = ('name', )

    name = factory.Sequence(lambda n: 'name{0}' .format(n))
    surname = factory.Sequence(lambda n: 'surname{0}'.format(n))
    address = factory.Sequence(lambda n: 'address{0}'.format(n))
    email = factory.LazyAttribute(lambda obj: '{0}@example.com'.format(
        obj.name))
