"""
django-extensions dumpscript import_help for TAO.

The help is currently written on the assumption that we only want to import
metadata in to a clean database, and not users or existing jobs.
"""
import sys
from django.contrib.auth.models import User as DjangoUser
from tao.models import Job, TaoUser, GlobalParameter

def locate_object(original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
    # Ignore Jobs, Users and UserProfiles
    if original_class in [DjangoUser, Job, TaoUser]:
        return original_class()
    search_data = { pk_name: pk_value }
    the_obj =the_class.objects.get(**search_data)
    return the_obj



def save_or_locate(the_obj):
    # Ignore Jobs, Users and UserProfiles
    if the_obj.__class__ in [DjangoUser, Job, TaoUser]:
        return the_obj

    # Update existing GlobalParameters
    if the_obj.__class__ == GlobalParameter:
        gps = GlobalParameter.objects.filter(parameter_name=the_obj.parameter_name)
        if gps:
            gp = gps[0]
            the_obj.pk = gp.pk

    # Save if we got here
    the_obj.save()
    return the_obj
