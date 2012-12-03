"""
    module responsible for constructing the parameters
"""

from lxml import etree

from tao import models
from tao.models import StellarModel

def param(name, value, **attrs):
    attrs['name'] = name
    return {
        'attrs': attrs,
        'value': value,
    }


def to_xml(light_cone_params, sed_params):
    """
        takes a list of dicts:
            {
                'attrs': {
                    'name': 'database',
                },
                'value': 'sqlite://sfh_bcgs200_full_z0.db',
            },
    """
    root = etree.Element('tao', timestamp='2012-11-13 13:45:32+1000', version='1.0')

    workflow = etree.SubElement(root, 'workflow', name='alpha-light-cone-image')

    light_cone_module = etree.SubElement(workflow, 'module', name='light-cone')

    _add_parameters(light_cone_module, light_cone_params)
    
    sed_module = etree.SubElement(workflow, 'module', name='sed')
    
    _add_parameters(sed_module, sed_params)

    return etree.tostring(root, pretty_print=True)

def _add_parameters(parameter_root, params):
    for param in params:
        parameter = etree.SubElement(parameter_root, 'param', **param['attrs'])
        parameter.text = unicode(param['value'])

def save(user, light_cone_form, sed_form):
        job = models.Job(user=user, parameters=_make_parameters(light_cone_form, sed_form))
        job.save()
        return job

def _make_parameters(light_cone_form, sed_form):
    from tao.datasets import NO_FILTER

    simulation = models.Simulation.objects.get(pk=light_cone_form.cleaned_data['dark_matter_simulation'])

    selected_filter = light_cone_form.cleaned_data['filter']
    if selected_filter != NO_FILTER:
        filter_parameter = models.DataSetParameter.objects.get(pk=selected_filter)
    else:
        filter_parameter = None

    light_cone_parameters = [
        param('database', 'sqlite://sfh_bcgs200_full_z0.db'),
        param('schema-version', '1.0'),
        param('query-type', light_cone_form.cleaned_data['box_type']),
        param('simulation-box-size', simulation.box_size, units=simulation.box_size_units),
        param('ra-min', light_cone_form.cleaned_data['ra_min'], units='deg'),
        param('ra-max', light_cone_form.cleaned_data['ra_max'], units='deg'),
        param('dec-min', light_cone_form.cleaned_data['dec_min'], units='deg'),
        param('dec-max', light_cone_form.cleaned_data['dec_max'], units='deg'),
    ]
    if filter_parameter is not None:
        light_cone_parameters.append(param('filter-type', filter_parameter.name))
        filter_min = light_cone_form.cleaned_data['min']
        filter_max = light_cone_form.cleaned_data['max']
        if filter_min != '':
            light_cone_parameters.append(param('filter-min', filter_min, units='Mpc'))
        if filter_max != '':
            light_cone_parameters.append(param('filter-max', filter_max, units='Mpc'))

    single_stellar_population_model = StellarModel.objects.get(pk=sed_form.cleaned_data['single_stellar_population_model'])
    sed_parameters = [
        param('single-stellar-population-model', single_stellar_population_model.name),
    ]
    
    return to_xml(light_cone_parameters, sed_parameters)