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

    paper_title = models.CharField(max_length=100, default='')
    paper_url = models.URLField(max_length=200, default='')
    external_link_url = models.URLField(max_length=200, default='')
    cosmology = models.CharField(max_length=100, default='')
    cosmological_parameters = models.CharField(max_length=100, default='')
    box_size_units = models.CharField(max_length=10, default='Mpc')
    box_size = models.DecimalField(max_digits=10, decimal_places=3)
    web_site = models.URLField(max_length=200, default='')

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
    kind = models.CharField(max_length=100, default='')
    paper_title = models.CharField(max_length=100, default='')
    paper_url = models.URLField(max_length=200, default='')

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        super(GalaxyModel, self).save(*args, **kwargs)
    
class DataSet(models.Model):
    simulation = models.ForeignKey(Simulation)
    galaxy_model = models.ForeignKey(GalaxyModel)
    database = models.CharField(max_length=200)
    min_snapshot = models.DecimalField(max_digits=10, decimal_places=9)
    max_snapshot = models.DecimalField(max_digits=10, decimal_places=9)
    
    class Meta:
        unique_together = ('simulation', 'galaxy_model')

    def __unicode__(self):
        return "%s : %s" % (self.simulation.name, self.galaxy_model.name)
    
class DataSetParameter(models.Model):
    name = models.CharField(max_length=200)
    units = models.CharField(max_length=20)
    label = models.CharField(max_length=40)
    dataset = models.ForeignKey(DataSet)
    
    def __unicode__(self):
        return self.label

    def option_label(self):
        return "%s (%s)" % (self.label, self.units)

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
    STATUS_CHOICES = (
        (SUBMITTED, 'Submitted'),
        (QUEUED, 'Queued'),
        (IN_PROGRESS, 'In progress'),
        (COMPLETED, 'Completed'),
    )

    user = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500)

    status = models.CharField(choices=STATUS_CHOICES, default=SUBMITTED, max_length=20)
    parameters = models.TextField(blank=True, max_length=1000000)
    output_path = models.TextField(blank=True)  # without a trailing slash, please

    def __unicode__(self):
        return "%s %s %s" % (self.user, self.created_time, self.description)

    def is_completed(self):
        return self.status == Job.COMPLETED

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
