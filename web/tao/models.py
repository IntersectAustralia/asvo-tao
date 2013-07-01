"""
==================
tao.models
==================

Database model mapping
"""
import django.contrib.auth.models as auth_models
from django.conf import settings
from django.db import models
from tao.mail import send_mail

import os

class UserManager(auth_models.UserManager):
    def admin_emails(self):
        return [x[0] for x in TaoUser.objects.filter(is_active=True, is_staff=True).values_list('email')]
    
class TaoUser(auth_models.AbstractUser):
    RS_NA = 'NA'
    RS_EMPTY = 'EMP'
    RS_PENDING = 'PEN'
    RS_APPROVED = 'APR'
    RS_REJECTED = 'REJ'

    objects = UserManager()

    institution = models.CharField(max_length=100, null=True)
    scientific_interests = models.CharField(max_length=500, null=True)
    title = models.CharField(max_length=5, null=True)
    rejected = models.BooleanField(default=False)
    aaf_shared_token = models.CharField(max_length=64, null=True, blank=True, default='')
    account_registration_status = models.CharField(max_length=3, blank=False, default=RS_NA)
    account_registration_reason = models.TextField(null=True, blank=True, default='')
    account_registration_date = models.DateTimeField(null=True)

    def display_name(self):
        if self.aaf_shared_token is not None and len(self.aaf_shared_token)>0:
            return self.first_name + ' (via AAF)'
        else:
            return self.username

    def display_registration_status(self):
        messages = {
            TaoUser.RS_NA: 'Not Applicable',
            TaoUser.RS_EMPTY: 'No registration form',
            TaoUser.RS_PENDING: 'Pending approval',
            TaoUser.RS_APPROVED: 'Account approved',
            TaoUser.RS_REJECTED: 'Registration rejected',
            }
        return messages[self.account_registration_status]

    def is_aaf(self):
        return self.account_registration_status in [TaoUser.RS_EMPTY, TaoUser.RS_APPROVED, TaoUser.RS_PENDING, TaoUser.RS_REJECTED]

    def is_rejected(self):
        return self.account_registration_status == TaoUser.RS_REJECTED

    def __unicode__(self):
        return "(%d) %s, %s" % (self.id, self.username, self.account_registration_status)

class Simulation(models.Model):        

    name = models.CharField(max_length=100, unique=True)
    box_size_units = models.CharField(max_length=10, default='Mpc')
    box_size = models.DecimalField(max_digits=10, decimal_places=3)
    details = models.TextField(default='')
    order = models.IntegerField(default='0')

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

    box_size_with_units.short_description = 'Box size'

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
    group = models.CharField(max_length=80, default='', blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['group', 'order', 'label']

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
    description = models.TextField(default='')

    def __unicode__(self):
        return self.name

def initial_job_status():
    try:
        obj = GlobalParameter.objects.get(parameter_name='INITIAL_JOB_STATUS')
        return obj.parameter_value.strip()
    except GlobalParameter.DoesNotExist:
        try:
            return getattr(settings,'INITIAL_JOB_STATUS')
        except AttributeError:
            return 'HELD'

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

class Job(models.Model):
    SUBMITTED = 'SUBMITTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    QUEUED = 'QUEUED'
    HELD = 'HELD'
    ERROR = 'ERROR'

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, default='')

    status = models.CharField(choices=STATUS_CHOICES, default=initial_job_status, max_length=20)
    parameters = models.TextField(blank=True, max_length=1000000)
    output_path = models.TextField(blank=True)  # without a trailing slash, please
    database = models.CharField(max_length=200)
    error_message = models.TextField(blank=True, max_length=1000000, default='')

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.var_cache = {}
        for var in ['status']:
            self.var_cache[var] = getattr(self, var)

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

    def files_tree(self):
        if not self.is_completed():
            raise Exception("can't look at files of job that is not completed")

        job_base_dir = os.path.join(settings.FILES_BASE, self.output_path)

        def traverse(path):
            for fn in os.listdir(path):
                child_path = os.path.join(path, fn)
                if os.path.isdir(child_path):
                    yield (child_path, traverse(child_path))
                else:
                    yield (child_path, None)

        #for data in traverse(job_base_dir):
        #    yield data
        return traverse(job_base_dir)

    def username(self):
        """ used by api """
        return self.user.username

    def can_read_job(self, user):
        """
        Checks if the given user is the user of this job
        """
        return self.user.id == user.id

    def can_download_zip_file(self):
        return True

    def save(self, *args, **kwargs):
        super(Job, self).save(*args, **kwargs)
        if self.var_cache['status'] != getattr(self, 'status') and getattr(self, 'status') == Job.COMPLETED:
            send_mail('job-status', {'job': self, 'user': self.user}, 'Job status update', (self.user.email,))
    
class JobFile(object):
    def __init__(self, job_dir, file_name):
        self.file_name = file_name[len(job_dir)+1:]
        self.file_path = os.path.join(job_dir, file_name)
        self.file_size = os.path.getsize(self.file_path)
    
    def can_be_downloaded(self):
        return True

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
    group = models.CharField(max_length=80, default='', blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['group', 'order', 'label']

    def __unicode__(self):
        return self.label

class DustModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    details = models.TextField(default='')

    def __unicode__(self):
        return self.label

class WorkflowCommand(models.Model):
    JOB_STOP_ALL = "Job_Stop_All"
    JOB_STOP = "Job_Stop"
    WORKFLOW_STOP = "Workflow_Stop"
    WORKFLOW_RESUME = "Workflow_Resume"
    JOB_OUTPUT_DELETE = "Job_Output_Delete"
    COMMAND_CHOICES = (
        (JOB_STOP_ALL, "Job Stop All"),
        (JOB_STOP, "Job Stop"),
        (WORKFLOW_STOP, "Workflow Stop"),
        (WORKFLOW_RESUME, "Workflow Resume"),
        (JOB_OUTPUT_DELETE, "Job Output Delete"),
    )

    job_id = models.ForeignKey(Job)
    issued = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(TaoUser)
    command = models.CharField(choices=COMMAND_CHOICES, max_length=64)
    parameters = models.CharField(max_length=1024, default='', blank=True)
    executed = models.DateTimeField(null=True, blank=True)
    execution_status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    execution_comment = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.command

    def jobid(self):
        return self.job_id.pk

    def submittedby(self):
        return self.submitted_by.pk

class GlobalParameter(models.Model):
    parameter_name = models.CharField(max_length=60, unique=True)
    parameter_value = models.TextField(default='')
    description = models.TextField(default='')

    def __str__(self):
        return self.parameter_name

