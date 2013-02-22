import factory
# http://factoryboy.readthedocs.org/en/latest/index.html

from decimal import Decimal

from tao.models import Job, User, Simulation, GalaxyModel, DataSet, DataSetProperty, StellarModel, Snapshot, BandPassFilter, DustModel

class JobFactory(factory.Factory):
    FACTORY_FOR = Job
    database = factory.Sequence(lambda n: 'database_' + n)
    description = factory.Sequence(lambda n: 'description job ' + n)
    
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
    box_size = factory.Sequence(lambda n: 10 * (int(n)+1))
    details = factory.Sequence(lambda n:
                                '<a class="simulation-paper" target="_blank" href="http://www.abcd' + n + '.com/">abcd' + n + '</a>' +
                                '<a class="simulation-link" target="_blank" href="http://www.defg' + n + '.org/">http://www.defg' + n + '.org/</a>' +
                                '<span class="simulation-cosmology">fairy' + n + '</span>' +
                                '<span class="simulation-cosmological-parameters">dust' + n + '</span>' +
                                '<span class="simulation-box-size">' + n + '</span>' +
                                '<a class="simulation-web-site" target="_blank" href="http://mysite' + n + '.edu/">http://mysite' + n + '.edu/</a>'
                                )
    
class GalaxyModelFactory(factory.Factory):
    FACTORY_FOR = GalaxyModel

    name = factory.Sequence(lambda n: 'galaxy_model_%03d' % int(n))
    details = factory.Sequence(lambda n:
                                'Kind: <span class="galaxy-model-kind">' + 'sometype' + n + '</span>' +
                                'Paper: <a class="galaxy-model-paper" target="_blank" href="' + 'http://www.xyz' + n + '.com/' + '">' + 'xyz' + n + '</a>'
                                )

class DataSetFactory(factory.Factory):
    FACTORY_FOR = DataSet
    
class DataSetPropertyFactory(factory.Factory):
    FACTORY_FOR = DataSetProperty
    label = factory.Sequence(lambda n: 'parameter_%03d' % int(n))
    name = factory.Sequence(lambda n: 'name_%03d' % int(n))
    data_type = DataSetProperty.TYPE_INT

class StellarModelFactory(factory.Factory):
    FACTORY_FOR = StellarModel

class SnapshotFactory(factory.Factory):
    FACTORY_FOR = Snapshot

    redshift = factory.Sequence(lambda n: str(int(n)/10.))

class BandPassFilterFactory(factory.Factory):
    FACTORY_FOR = BandPassFilter
    label = factory.Sequence(lambda n: 'Band pass filter %03d' % int(n))
    filter_id = factory.Sequence(lambda n: 'Band_pass_filter_%03d.txt' % int(n))

class DustModelFactory(factory.Factory):
    FACTORY_FOR = DustModel
    name = factory.Sequence(lambda n: 'Dust_model_%03d.dat' % int(n))
    label = factory.Sequence(lambda n: 'Dust model %03d' % int(n))