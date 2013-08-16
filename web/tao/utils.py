"""
Module: tao.utils

Description:

Convenience routines for TAO.
"""
from tao.models import GlobalParameter

def output_formats():
    """Answer the list of supported output formats."""
    of_string = GlobalParameter.objects.get(parameter_name="output_formats").parameter_value
    return eval(of_string.replace('\r',''))
