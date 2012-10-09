import factory
# http://factoryboy.readthedocs.org/en/latest/index.html

from tao.models import Job, User

class JobFactory(factory.Factory):
    FACTORY_FOR = Job

class UserFactory(factory.Factory):
    FACTORY_FOR = User
