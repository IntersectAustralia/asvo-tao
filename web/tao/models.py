"""
==================
tao.models
==================

Database model mapping
"""
import django.contrib.auth.models as auth_models
from django.conf import settings
from django.db import models

import os

class UserProfile(models.Model):
    user = models.OneToOneField(auth_models.User)

    institution = models.CharField(max_length=100)
    scientific_interests = models.CharField(max_length=500)
    title = models.CharField(max_length=5)
    rejected = models.BooleanField(default=False)


class UserManager(auth_models.UserManager):
    def admin_emails(self):
        return [x[0] for x in User.objects.filter(is_active=True, is_staff=True).values_list('email')]
    
    
class User(auth_models.User):
    """
        Wrapper to make methods on user_profile one call
    """
    objects = UserManager()
    def title(self):
        # TODO This probably makes too many SQL queries by default?
        return self.get_profile().title

    class Meta:
        proxy = True
    
class Simulation(models.Model):        

    name = models.CharField(max_length=100, unique=True)
    box_size_units = models.CharField(max_length=10, default='Mpc')
    box_size = models.DecimalField(max_digits=10, decimal_places=3)
    details = models.TextField(default='')

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        super(Simulation, self).save(*args, **kwargs)

    def box_size_with_units(self):
        return "%s %s" % (self.box_size, self.box_size_units)

class GalaxyModel(models.Model):

    simulation_set = models.ManyToManyField(Simulation, through='DataSet')
    name = models.CharField(max_length=100, unique=True)
    details = models.TextField(default='')

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        super(GalaxyModel, self).save(*args, **kwargs)
    
class DataSet(models.Model):
    """A DataSet is the stored output of running a GalaxyModel over a Simulation.
    
    Fields:
        database: The name of the database storing the DataSet.
                    This must match the name used by the back-end workflow.
        version: The DataSet version.  Not currently used.
        import_date: The date the DataSet metadata was first imported.
                    As this will typically be created by the back-end dataset
                    import script, it will match the DataSet import date.
        available: Flag whether to allow use of the DataSet from the web UI.
                    Not currently used."""
    simulation = models.ForeignKey(Simulation)
    galaxy_model = models.ForeignKey(GalaxyModel)
    database = models.CharField(max_length=200)
    version = models.DecimalField(max_digits=10, decimal_places=2, default='1.00')
    import_date = models.DateField(auto_now_add=True)
    available = models.BooleanField(default=True)
    default_filter_field = models.ForeignKey('DataSetProperty', related_name='DataSetProperty', null=True, blank=True)
    default_filter_min = models.FloatField(null=True, blank=True)
    default_filter_max = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ('simulation', 'galaxy_model')

    def __unicode__(self):
        return "%s : %s" % (self.simulation.name, self.galaxy_model.name)

class DataSetProperty(models.Model):
    TYPE_INT = 0
    TYPE_FLOAT = 1
    TYPE_LONG_LONG = 2
    TYPE_STRING = 3
    # Note: The values listed below are used by the import code,
    # and thus must match.
    DATA_TYPES = (
                  (TYPE_INT, 'int'),
                  (TYPE_FLOAT, 'float'),
                  (TYPE_LONG_LONG, 'long long'),
                  (TYPE_STRING, 'string'),
                  )
    name = models.CharField(max_length=200)
    units = models.CharField(max_length=20, default='', blank=True)
    label = models.CharField(max_length=40)
    dataset = models.ForeignKey(DataSet)
    data_type = models.IntegerField(choices=DATA_TYPES)
    is_computed = models.BooleanField(default=False)
    is_filter = models.BooleanField(default=True)
    is_output = models.BooleanField(default=True)
    description = models.TextField(default='', blank=True)
    
    def __unicode__(self):
        return self.label

    def option_label(self):
        if (self.units is not None and self.units != ''):
            return "%s (%s)" % (self.label, self.units)
        else:
            return self.label

    @classmethod
    def data_type_enum(cls, val):
        for dtype in cls.DATA_TYPES:
            if dtype[1] == val:
                return dtype[0]
        raise ValueError('Unknown data type')


class Snapshot(models.Model):
    dataset = models.ForeignKey(DataSet)
    redshift = models.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        unique_together = ('dataset', 'redshift')

class StellarModel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    label = models.CharField(max_length=200, unique=True)
    
    def __unicode__(self):
        return self.name
    
class Job(models.Model):
    SUBMITTED = 'SUBMITTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    QUEUED = 'QUEUED'
    HELD = 'HELD'
    ERROR = 'ERROR'
    STATUS_CHOICES = (
        (SUBMITTED, 'Submitted'),
        (QUEUED, 'Queued'),
        (IN_PROGRESS, 'In progress'),
        (COMPLETED, 'Completed'),
        (HELD, 'Held'),
        (ERROR, 'Error'),
    )

    user = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, default='')

    status = models.CharField(choices=STATUS_CHOICES, default=HELD, max_length=20)
    parameters = models.TextField(blank=True, max_length=1000000)
    output_path = models.TextField(blank=True)  # without a trailing slash, please
    database = models.CharField(max_length=200)
    error_message = models.TextField(blank=True, max_length=1000000, default='')

    def __unicode__(self):
        return "%s %s %s" % (self.user, self.created_time, self.description)

    def is_completed(self):
        return self.status == Job.COMPLETED

    def is_error(self):
        return self.status == Job.ERROR

    def short_error_message(self):
        return self.error_message[:80]

    def files(self):
        if not self.is_completed():
            raise Exception("can't look at files of job that is not completed")
        
        all_files = []
        job_base_dir = os.path.join(settings.FILES_BASE, self.output_path)
        for root, dirs, files in os.walk(job_base_dir):
            all_files += [JobFile(job_base_dir, os.path.join(root, filename)) for filename in files]
        return sorted(all_files, key=lambda job_file: job_file.file_name)

    def username(self):
        """ used by api """
        return self.user.username

    def can_read_job(self, user):
        """
        Checks if the given user is the user of this job
        """
        return self.user.id == user.id

    def can_download_zip_file(self):
        sum_size = 0
        for file in self.files():
            file_path = file.file_path 
            sum_size += os.path.getsize(file_path)
        return sum_size < settings.MAX_DOWNLOAD_SIZE
    
class JobFile(object):
    def __init__(self, job_dir, file_name):
        self.file_name = file_name[len(job_dir)+1:]
        self.file_path = os.path.join(job_dir, file_name)
        self.file_size = os.path.getsize(self.file_path)
    
    def can_be_downloaded(self):
        return self.file_size <= settings.MAX_DOWNLOAD_SIZE

    def get_file_size(self):
        size = self.file_size
        units = ['B', 'kB', 'MB']
        for x in units:
            if size < 1000:
                return '%3.1f%s' % (size, x)
            size /= 1000
        return '%3.1f%s' % (size, 'GB')

class BandPassFilter(models.Model):
    label = models.CharField(max_length=80) # displays the user-friendly file name for the filter, without file extension
    filter_id = models.CharField(max_length=200, unique=True) # full file name of the filter data, as an internal identifier
    description = models.TextField(default='') # when a single band pass filter is selected, this will be displayed in a new details panel on the right

    def __unicode__(self):
        return self.label

class DustModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    details = models.TextField(default='')

    def __unicode__(self):
        return self.label
