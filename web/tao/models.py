import django.contrib.auth.models as auth_models
from django.db import models


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
    name = models.CharField(max_length=100)

    paper_title = models.CharField(max_length=100, default='')
    paper_url = models.URLField(max_length=200, default='')
    external_link_url = models.URLField(max_length=200, default='')
    cosmology = models.CharField(max_length=100, default='')
    cosmological_parameters = models.CharField(max_length=100, default='')
    box_size = models.CharField(max_length=100, default='')
    web_site = models.URLField(max_length=200, default='')

    def __unicode__(self):
        return self.name


class GalaxyModel(models.Model):
    simulation = models.ForeignKey(Simulation)

    name = models.CharField(max_length=100)

    kind = models.CharField(max_length=100, default='')
    paper_title = models.CharField(max_length=100, default='')
    paper_url = models.URLField(max_length=200, default='')

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
