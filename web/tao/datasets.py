"""
    functionality for:
        * dark matter simulations
        * galaxy models
        * stellar models
"""

from . import models

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

def filter_choices(data_set_id):
    dataset = models.DataSet.objects.get(id=data_set_id)
    return models.DataSetProperty.objects.filter(dataset_id = dataset.id, is_filter = True).order_by('name')

def stellar_model_choices():
    """
        for now the SED has a single selection value, which is still TBD.
    """
    return [(x.id, x.name, {}) for x in models.StellarModel.objects.order_by('name')]

def snapshot_choices():
    return [(x.id, str(x.redshift), {'data-galaxy_model_id': str(x.dataset.galaxy_model_id), 'data-simulation_id': str(x.dataset.simulation_id)})
            for x in models.Snapshot.objects.order_by('redshift')]
