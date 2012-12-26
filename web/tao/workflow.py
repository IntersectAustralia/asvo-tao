"""
    module responsible for constructing the parameters
"""

from lxml import etree

from tao import models, time
from tao.models import StellarModel

from decimal import Decimal

def param(name, value, **attrs):
    attrs['name'] = name
    if isinstance(value, Decimal):
        if 'E' in str(value):
            value = "%.20g" % value
    return {
        'attrs': attrs,
        'value': value,
    }


def to_xml(common_params, light_cone_params, sed_params):
    """
        takes a list of dicts:
            {
                'attrs': {
                    'name': 'database',
                },
                'value': 'sqlite://sfh_bcgs200_full_z0.db',
            },
    """
    root = etree.Element('tao', xmlns='http://tao.asvo.org.au/schema/module-parameters-v1', timestamp=time.timestamp())

    workflow = etree.SubElement(root, 'workflow', name='alpha-light-cone-image')

    _add_parameters(workflow, common_params)

    light_cone_module = etree.SubElement(workflow, 'module', name='light-cone')

    _add_parameters(light_cone_module, light_cone_params)

    sed_module = etree.SubElement(workflow, 'module', name='sed')
    
    _add_parameters(sed_module, sed_params)

    filter_module = etree.SubElement(workflow, 'module', name='filter')
    filter_inner = etree.SubElement(filter_module, 'filter')
    waves_filename = etree.SubElement(filter_inner, 'waves_filename')
    waves_filename.text = 'wavelengths.dat'
    filter_filenames = etree.SubElement(filter_inner, 'filter_filenames')
    filter_filenames.text = 'u.dat,v.dat,zpv.dat,k.dat,zpk.dat'
    vega_filename = etree.SubElement(filter_inner, 'vega_filename')
    vega_filename.text = 'A0V_KUR_BB.SED'

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
    # precondition: forms are valid

    from tao.datasets import NO_FILTER
    from tao.forms import LightConeForm
     
    simulation = models.Simulation.objects.get(pk=light_cone_form.cleaned_data['dark_matter_simulation'])
    galaxy_model = models.GalaxyModel.objects.get(pk=light_cone_form.cleaned_data['galaxy_model'])
    dataset = models.DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)

    selected_filter = light_cone_form.cleaned_data['filter']
    if selected_filter != NO_FILTER:
        filter_parameter = models.DataSetParameter.objects.get(pk=selected_filter)
    else:
        filter_parameter = None

    if light_cone_form.cleaned_data['catalogue_geometry'] == LightConeForm.BOX:
        redshift_min = light_cone_form.cleaned_data['snapshot']
        redshift_max = light_cone_form.cleaned_data['snapshot']
    else:
        redshift_min = light_cone_form.cleaned_data['redshift_min']
        redshift_max = light_cone_form.cleaned_data['redshift_max']

    common_parameters = [
        param('database-type', 'postgresql'),
        param('database-host', 'tao02.hpc.swin.edu.au'),
        param('database-name', 'millennium_full'),
        param('database-port', '3306'),
        param('database-user', ''),
        param('database-pass', ''),
        param('schema-version', '1.0'),
    ]

    light_cone_parameters = [
        param('query-type', light_cone_form.cleaned_data['catalogue_geometry']),
        param('simulation-box-size', simulation.box_size, units=simulation.box_size_units),
        param('redshift-min', redshift_min),
        param('redshift-max', redshift_max),
    ]
    if light_cone_form.cleaned_data['catalogue_geometry'] == LightConeForm.CONE:
        light_cone_parameters += [
            param('ra-min', 0, units='deg'),
            param('ra-max', light_cone_form.cleaned_data['ra_opening_angle'], units='deg'),
            param('dec-min', 0, units='deg'),
            param('dec-max', light_cone_form.cleaned_data['dec_opening_angle'], units='deg'),
        ]
    elif light_cone_form.cleaned_data['catalogue_geometry'] == LightConeForm.BOX:
        light_cone_parameters += [
            param('query-box-size', light_cone_form.cleaned_data['box_size']),
        ]
        
    if filter_parameter is not None:
        light_cone_parameters.append(param('filter-type', filter_parameter.name))
        filter_min = light_cone_form.cleaned_data['min']
        filter_max = light_cone_form.cleaned_data['max']
        if filter_min != '':
            light_cone_parameters.append(param('filter-min', filter_min, units=filter_parameter.units))
        if filter_max != '':
            light_cone_parameters.append(param('filter-max', filter_max, units=filter_parameter.units))

    single_stellar_population_model = StellarModel.objects.get(pk=sed_form.cleaned_data['single_stellar_population_model'])
    sed_parameters = [
        param('single-stellar-population-model', single_stellar_population_model.name),
    ]
    
    return to_xml(common_parameters, light_cone_parameters, sed_parameters)
