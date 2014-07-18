"""
================
tao.datasets
================

"""
from decimal import Decimal
from django.db.models import Q
from tao import models


def remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

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
    return [(x.id, x.name, {}) for x in models.Simulation.objects.order_by('order', 'name')]

    # TODO: 'sid' doesn't do anything
def galaxy_model_choices(sid):
    """
        return tuples of galaxy model choices suitable for use in a
        tao.widgets.ChoiceFieldWithOtherAttrs
    """
    return [(x.id, x.name, {})
            for x in models.GalaxyModel.objects.order_by('name')]

def stellar_model_choices():
    """
        for now the SED has a single selection value, which is still TBD.
    """
    return [(x.id, x.label, {}) for x in models.StellarModel.objects.order_by('label')]

# TODO: This should only return the redshifts from the selected dataset
# This is no longer used to populate the Redshift dropdown, but is used 
# by the unit test.  Possibly move inside the unit test.
def snapshot_choices(dataset_id):
    return [(x.id, str(x.redshift),{})
            for x in models.Snapshot.objects.filter(dataset=dataset_id).order_by('redshift')]

def filter_choices(simulation_id, galaxy_model_id):
    try:
        dataset = models.DataSet.objects.get(simulation_id=simulation_id, galaxy_model_id=galaxy_model_id)
        dataset_id = dataset.id
        dataset_default_filter = dataset.default_filter_field
    except models.DataSet.DoesNotExist:
        dataset_id = None
        dataset_default_filter = None
    q = Q(dataset_id = dataset_id, is_filter=True)
    if dataset_default_filter is not None: q = q | Q(pk=dataset.default_filter_field.id)
    return models.DataSetProperty.objects.filter(q).exclude(data_type = models.DataSetProperty.TYPE_STRING).order_by('name')

def output_choices(data_set_id):
    try:
        dataset = models.DataSet.objects.get(id=data_set_id)
        dataset_id = dataset.id
    except models.DataSet.DoesNotExist:
        dataset_id = None
    return models.DataSetProperty.objects.filter(dataset_id = dataset_id, is_output = True).order_by('group', 'order', 'label')
def SortProperties(PropArr):
    return models.DataSetProperty.getSortedList(PropArr)	
    
def output_property(id):
    return models.DataSetProperty.objects.get(pk=id, is_output=True)

def band_pass_filters_objects():
    return models.BandPassFilter.objects.order_by('group', 'order', 'label')

def band_pass_filters_enriched():
    def gen_pairs(objs):
        for obj in objs:
            yield (str(obj.id) + '_apparent', obj.label + ' (Apparent)')
            yield (str(obj.id) + '_absolute', obj.label + ' (Absolute)')
    return [pair for pair in gen_pairs(band_pass_filters_objects())]

def band_pass_filter(id):
    id_num = id
    if '_' in id:
        id_num = id[0:id.index('_')]
    return models.BandPassFilter.objects.get(pk=id_num)

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
    if filter_type is None:
        return ('E', 0)
    try:
        obj = models.DataSetProperty.objects.get(name=filter_type, units=filter_units, dataset__pk=data_set_id)
        return ('D', obj.id)
    except models.DataSetProperty.DoesNotExist:
        suffix = ''
        if filter_type.endswith('_apparent'):
            filter_type = filter_type[:-len('apparent')-1]
            suffix = '_apparent'
        elif filter_type.endswith('_absolute'):
            filter_type = filter_type[:-len('absolute')-1]
            suffix = '_absolute'
        try:
            obj = models.BandPassFilter.objects.get(filter_id=filter_type)
            return ('B', str(obj.id) + suffix)
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
        # redshift may be a String, Decimal, Float or Integer
        # If a string, it may be simple or scientific format
        # MySQL / Python 2.6 is a problem...
        # Convert to normalised Decimal and hope for the best
        obj = models.Snapshot.objects.get(dataset=data_set, redshift=remove_exponent(Decimal(redshift)))
        return obj
    except models.Snapshot.DoesNotExist:
        return None

def simulation_from_xml(simulation_name):
    try:
        obj = models.Simulation.objects.get(name=simulation_name)
        return obj
    except models.Simulation.DoesNotExist:
        return None

def galaxy_model_from_xml(galaxy_model_name):
    try:
        obj = models.GalaxyModel.objects.get(name=galaxy_model_name)
        return obj
    except models.GalaxyModel.DoesNotExist:
        return None

def data_set_property_from_xml(data_set, label, name):
    try:
        obj = models.DataSetProperty.objects.get(dataset=data_set, name=name)
        return obj
    except models.DataSetProperty.DoesNotExist:
        return None
