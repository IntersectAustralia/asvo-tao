import factory
# http://factoryboy.readthedocs.org/en/latest/index.html

from tao.models import Job, User

class JobFactory(factory.Factory):
    FACTORY_FOR = Job

class UserFactory(factory.Factory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'username' + n)
    email = factory.Sequence(lambda n: 'email' + n + '@example.com')