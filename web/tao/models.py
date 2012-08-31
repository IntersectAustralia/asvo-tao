import django.contrib.auth.models as auth_models
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(auth_models.User)

    institution = models.CharField(max_length=100)
    scientific_interests = models.CharField(max_length=500)
    title = models.CharField(max_length=5)
    rejected = models.BooleanField(default=False)


class User(auth_models.User):
    """
        Wrapper to make methods on user_profile one call
    """
    def title(self):
        # TODO This probably makes too many SQL queries by default?
        return self.get_profile().title

    class Meta:
        proxy = True
