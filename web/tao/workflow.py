"""
    module responsible for constructing the parameters
"""

from lxml import etree


def param(name, value, **attrs):
    attrs['name'] = name
    return {
        'attrs': attrs,
        'value': value,
    }


def to_xml(params):
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

    parameters = etree.SubElement(workflow, 'module', name='light-cone')

    _add_parameters(parameters, params)

    return etree.tostring(root, pretty_print=True)

def _add_parameters(parameter_root, params):
    for param in params:
        parameter = etree.SubElement(parameter_root, 'param', **param['attrs'])
        parameter.text = unicode(param['value'])
