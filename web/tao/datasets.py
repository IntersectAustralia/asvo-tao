"""
    functionality for:
        * dark matter simulations
        * galaxy models
        * stellar models
"""

from . import models


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
    return [(x.id, x.name, {'data-sim': unicode(x.simulation_id)}) for x in models.GalaxyModel.objects.order_by('name')]
