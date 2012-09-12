"""
    functionality for:
        * dark matter simulations
        * galaxy models
        * stellar models
"""

from . import models

def dark_matter_simulations():
    return models.Simulation.objects.all()
