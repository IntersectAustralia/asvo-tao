import factory
# http://factoryboy.readthedocs.org/en/latest/index.html

from decimal import Decimal

from tao.models import Job, User, Simulation, GalaxyModel, DataSet, DataSetParameter, StellarModel

class JobFactory(factory.Factory):
    FACTORY_FOR = Job
    
    @classmethod
    def _prepare(cls, create, **kwargs):
        created_time = kwargs.pop('created_time', None)
        job = super(JobFactory, cls)._prepare(create, **kwargs)
        if created_time:
            job.created_time = created_time
            if create:
                job.save()
        return job

class UserFactory(factory.Factory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'username' + n)
    email = factory.Sequence(lambda n: 'email' + n + '@example.com')
    
    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
    
class SimulationFactory(factory.Factory):
    FACTORY_FOR = Simulation
    name = factory.Sequence(lambda n: 'simulation_%03d' % int(n))
    paper_title = factory.Sequence(lambda n: "abcd" + n) 
    paper_url = factory.Sequence(lambda n: "http://www.abcd" + n + ".com/")
    external_link_url = factory.Sequence(lambda n: "http://www.defg" + n + ".org/")
    cosmology = factory.Sequence(lambda n: "fairy" + n)
    cosmological_parameters = factory.Sequence(lambda n: "dust" + n)
    box_size = factory.Sequence(lambda n: n)
    web_site = factory.Sequence(lambda n: "http://mysite" + n + ".edu/")
    
class GalaxyModelFactory(factory.Factory):
    FACTORY_FOR = GalaxyModel

    simulation = factory.SubFactory(SimulationFactory)

    name = factory.Sequence(lambda n: 'galaxy_model_%03d' % int(n))
    kind = factory.Sequence(lambda n: "sometype" + n) 
    paper_title = factory.Sequence(lambda n: "xyz" + n)
    paper_url = factory.Sequence(lambda n: "http://www.xyz" + n + ".com/")
    
class DataSetFactory(factory.Factory):
    FACTORY_FOR = DataSet
    min_snapshot = Decimal('0')
    max_snapshot = Decimal('1')
    
class DataSetParameterFactory(factory.Factory):
    FACTORY_FOR = DataSetParameter
    name = factory.Sequence(lambda n: 'parameter_%03d' % int(n))

class StellarModelFactory(factory.Factory):
    FACTORY_FOR = StellarModel
