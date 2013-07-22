"""
django-extensions dumpscript import_help for TAO.

The help is currently written on the assumption that we only want to import
metadata in to a clean database, and not users or existing jobs.
"""
import sys
from django.contrib.auth.models import User as DjangoUser
from tao.models import Job, TaoUser, GlobalParameter, Snapshot

# We only want to display some messages once.
# displayed_messages can be used to hold a flag indicating that the message
# has been displayed.
displayed_messages = []

ignored_classes = [DjangoUser, Job, TaoUser]

def locate_object(original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
    # Ignore Jobs, Users and UserProfiles
    if original_class in ignored_classes:
        if original_class not in ignored_classes:
            print("Ignoring {0}".format(str(original_class)))
            displayed_messages.append(original_class)
        return original_class()
    search_data = { pk_name: pk_value }
    the_obj =the_class.objects.get(**search_data)
    return the_obj



def save_or_locate(the_obj):
    # Ignore Jobs, Users and UserProfiles
    if the_obj.__class__ in [DjangoUser, Job, TaoUser]:
        if original_class not in ignored_classes:
            print("Ignoring {0}".format(str(original_class)))
            displayed_messages.append(original_class)
        return the_obj

    # Update existing GlobalParameters
    if the_obj.__class__ == GlobalParameter:
        gps = GlobalParameter.objects.filter(parameter_name=the_obj.parameter_name)
        if gps:
            gp = gps[0]
            the_obj.pk = gp.pk

    # Snapshots may have their dataset added later.
    # If we have a snapshot with no dataset, just return and assume
    # it will be updated and saved later
    if the_obj.__class__ == Snapshot:
        #import pdb; pdb.set_trace()
        if the_obj.dataset_id == None:
            if Snapshot not in displayed_messages:
                print("Ignoring Snapshot with no dataset")
                displayed_messages.append(Snapshot)
            return the_obj

    # Save if we got here
    the_obj.save()
    return the_obj
