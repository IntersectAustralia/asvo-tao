"""
    functionality for:
        * dark matter simulations
        * galaxy models
        * stellar models
"""

from . import models

NO_FILTER = 'no_filter'

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
    return [(x.id, x.name, {'data-simulation_id': unicode(x.simulation_id)}) for x in models.GalaxyModel.objects.order_by('name')]

def filter_choices():
    return [(NO_FILTER, 'No Filter', {})] + [(x.id, x.name, {
                            'data-simulation_id': unicode(x.dataset.simulation_id),
                            'data-galaxy_model_id': unicode(x.dataset.galaxy_model_id)
                            })
            for x in models.DataSetParameter.objects.order_by('name')]

def stellar_model_choices():
    """
        for now the SED has a single selection value, which is still TBD.
    """
    return [(x.id, x.name, {}) for x in models.StellarModel.objects.order_by('name')]
