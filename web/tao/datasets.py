"""
    functionality for:
        * dark matter simulations
        * galaxy models
        * stellar models
"""

from . import models


def dark_matter_simulation_choices():
    """ return """
    return [('label', 'value') for x in models.Simulation.objects.all()]


def galaxy_model_choices():
    return [(x.name, x.name) for x in models.GalaxyModel.objects.all()]
