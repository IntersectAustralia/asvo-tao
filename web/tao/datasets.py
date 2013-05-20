"""
================
tao.datasets
================

"""
from django.db.models import Q
from tao import models

def dataset_get(dataset_id):
    return models.DataSet.objects.get(pk=dataset_id)

def dataset_for_simulation_and_galaxy_model(simulation_id, galaxy_model_id):
    """
    returns _the_ dataset for a given simulation and galaxy model
    :param simulation_id:
    :param galaxy_model_id:
    :return: dataset object
    """
    return models.DataSet.objects.get(simulation_id=simulation_id, galaxy_model_id=galaxy_model_id)

def data_set_properties_for_record_filer(simulation_id, galaxy_model_id):
    """
        returns list of data set properties that are available as record filters
    :return:
    """
    return [x for x in models.DataSetProperty.objects.filter(is_filter=True, dataset=dataset_for_simulation_and_galaxy_model(simulation_id, galaxy_model_id))]

def dark_matter_simulation_choices():
    """
        return tuples of dark matter choices suitable for use in a
        tao.widgets.ChoiceFieldWithOtherAttrs
    """
    return [(x.id, x.name, {}) for x in models.Simulation.objects.order_by('name')]


def galaxy_model_choices():
    """
        return tuples of galaxy model choices suitable for use in a
        tao.widgets.ChoiceFieldWithOtherAttrs
    """
    return [(x.id, x.galaxy_model.name, {'data-galaxy_model_id': str(x.galaxy_model_id)}) for x in models.DataSet.objects.all().select_related('galaxy_model').order_by('galaxy_model__name')]

def stellar_model_choices():
    """
        for now the SED has a single selection value, which is still TBD.
    """
    return [(x.id, x.label, {}) for x in models.StellarModel.objects.order_by('label')]

def snapshot_choices():
    return [(x.id, str(x.redshift), {'data-galaxy_model_id': str(x.dataset.galaxy_model_id), 'data-simulation_id': str(x.dataset.simulation_id)})
            for x in models.Snapshot.objects.order_by('redshift')]

def filter_choices(data_set_id):
    try:
        dataset = models.DataSet.objects.get(id=data_set_id)
        dataset_id = dataset.id
        dataset_default_filter = dataset.default_filter_field
    except models.DataSet.DoesNotExist:
        dataset_id = None
        dataset_default_filter = None
    q = Q(dataset_id = dataset_id, is_filter=True)
    if dataset_default_filter is not None: q = q | Q(pk=dataset.default_filter_field.id)
    return models.DataSetProperty.objects.filter(q).exclude(data_type = models.DataSetProperty.TYPE_STRING).order_by('name')

def default_filter_choice(data_set_id):
    dataset = models.DataSet.objects.get(id=data_set_id)
    return dataset.default_filter_field

def default_filter_min(data_set_id):
    dataset = models.DataSet.objects.get(id=data_set_id)
    return dataset.default_filter_min

def default_filter_max(data_set_id):
    dataset = models.DataSet.objects.get(id=data_set_id)
    return dataset.default_filter_max

def output_choices(data_set_id):
    try:
        dataset = models.DataSet.objects.get(id=data_set_id)
        dataset_id = dataset.id
    except models.DataSet.DoesNotExist:
        dataset_id = None
    return models.DataSetProperty.objects.filter(dataset_id = dataset_id, is_output = True).order_by('group', 'order', 'label')

def output_property(id):
    return models.DataSetProperty.objects.get(pk=id, is_output=True)

def band_pass_filters():
    return [(x.id, x.label) for x in models.BandPassFilter.objects.order_by('label')]

def band_pass_filters_objects():
    return models.BandPassFilter.objects.order_by('group', 'order', 'label')

def band_pass_filter(id):
    return models.BandPassFilter.objects.get(pk=id)

def dust_models():
    return [(x.id, x.label) for x in models.DustModel.objects.order_by('label')]

def dust_models_objects():
    return models.DustModel.objects.order_by('label')

def dataset_find_from_xml(simulation, galaxy_model):
    try:
        obj = models.DataSet.objects.get(simulation__name=simulation, galaxy_model__name=galaxy_model)
        return obj
    except models.DataSet.DoesNotExist:
        return None

def filter_find_from_xml(data_set_id, filter_type, filter_units):
    try:
        obj = models.DataSetProperty.objects.get(name=filter_type, units=filter_units, dataset__pk=data_set_id)
        return ('D', obj.id)
    except models.DataSetProperty.DoesNotExist:
        try:
            obj = models.BandPassFilter.objects.get(filter_id=filter_type)
            return ('B', obj.id)
        except models.BandPassFilter.DoesNotExist:
            return ('E', 0)

def stellar_model_find_from_xml(name):
    try:
        obj = models.StellarModel.objects.get(name=name)
        return obj
    except models.StellarModel.DoesNotExist:
        return None

def band_pass_filter_find_from_xml(filter_id):
    try:
        obj = models.BandPassFilter.objects.get(filter_id=filter_id)
        return obj
    except models.BandPassFilter.DoesNotExist:
        return None

def dust_model_find_from_xml(name):
    try:
        obj = models.DustModel.objects.get(name=name)
        return obj
    except models.DustModel.DoesNotExist:
        return None

def snapshot_from_xml(data_set, redshift):
    try:
        obj = models.Snapshot.objects.get(dataset=data_set, redshift=redshift)
        return obj
    except models.Snapshot.DoesNotExist:
        return None

def simulation_from_xml(simulation_name):
    try:
        obj = models.Simulation.objects.get(name=simulation_name)
        return obj
    except models.Simulation.DoesNotExist:
        return None

def data_set_property_from_xml(data_set, label, name):
    try:
        obj = models.DataSetProperty.objects.get(dataset=data_set, label=label, name=name)
        return obj
    except models.DataSetProperty.DoesNotExist:
        return None
