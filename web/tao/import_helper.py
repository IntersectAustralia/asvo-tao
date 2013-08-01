"""
django-extensions dumpscript import_help for TAO.

The help is currently written on the assumption that we only want to import
metadata in to a clean database, and not users or existing jobs.
"""
import sys
from django.contrib.auth.models import User as DjangoUser
from tao.models import Job, TaoUser, GlobalParameter, Snapshot, WorkflowCommand
from tao.models import Simulation, GalaxyModel, DataSet, DataSetProperty


# We only want to display some messages once.
# displayed_messages can be used to hold a flag indicating that the message
# has been displayed.
displayed_messages = []

ignored_classes = [DjangoUser, Job, TaoUser, WorkflowCommand]



def save_or_locate(the_obj):
    # Ignore Jobs, Users and UserProfiles
    the_obj_class = the_obj.__class__
    if the_obj_class in ignored_classes:
        if the_obj_class not in displayed_messages:
            print("Ignoring {0}".format(str(the_obj_class)))
            displayed_messages.append(the_obj_class)
        return the_obj

    # Update existing GlobalParameters
    if the_obj.__class__ == GlobalParameter:
        orig_objs = GlobalParameter.objects.filter(
                        parameter_name=the_obj.parameter_name)
        if len(orig_objs) > 1:
            raise Exception("Found more than one original object")
        if len(orig_objs) == 1:
            orig_obj = orig_objs[0]
            the_obj.pk = orig_obj.pk

    # Update existing Simulations
    if the_obj.__class__ == Simulation:
        orig_objs = Simulation.objects.filter(name=the_obj.name)
        if len(orig_objs) > 1:
            raise Exception("Found more than one original object")
        if len(orig_objs) == 1:
            orig_obj = orig_objs[0]
            the_obj.pk = orig_obj.pk

    # Update existing GalaxyModels
    if the_obj.__class__ == GalaxyModel:
        orig_objs = GalaxyModel.objects.filter(name=the_obj.name)
        if len(orig_objs) > 1:
            raise Exception("Found more than one original object")
        if len(orig_objs) == 1:
            orig_obj = orig_objs[0]
            the_obj.pk = orig_obj.pk

    # Update existing DataSets
    if the_obj.__class__ == DataSet:
        orig_objs = DataSet.objects.filter(simulation=the_obj.simulation,
                galaxy_model=the_obj.galaxy_model)
        if len(orig_objs) > 1:
            raise Exception("Found more than one original object")
        if len(orig_objs) == 1:
            orig_obj = orig_objs[0]
            the_obj.pk = orig_obj.pk

    # Update existing DataSetProperties
    if the_obj.__class__ == DataSetProperty:
        orig_objs = DataSetProperty.objects.filter(
                name=the_obj.name,
                dataset=the_obj.dataset)
        if len(orig_objs) > 1:
            raise Exception("Found more than one original object")
        if len(orig_objs) == 1:
            orig_obj = orig_objs[0]
            the_obj.pk = orig_obj.pk


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
