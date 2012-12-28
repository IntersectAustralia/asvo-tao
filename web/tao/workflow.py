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

def add_parameters(parameter_root, params):
    for param in params:
        parameter = etree.SubElement(parameter_root, 'param', **param['attrs'])
        parameter.text = unicode(param['value'])

def save(user, forms):
    job = models.Job(user=user, parameters=_make_parameters(forms))
    job.save()
    return job

def _make_parameters(forms):
    # precondition: forms are valid

    root = etree.Element('tao', xmlns='http://tao.asvo.org.au/schema/module-parameters-v1', timestamp=time.timestamp())

    workflow = etree.SubElement(root, 'workflow', name='alpha-light-cone-image')

    common_parameters = [
        param('database-type', 'postgresql'),
        param('database-host', 'tao02.hpc.swin.edu.au'),
        param('database-name', 'millennium_full'),
        param('database-port', '3306'),
        param('database-user', ''),
        param('database-pass', ''),
        param('schema-version', '1.0'),
    ]
    add_parameters(workflow, common_parameters)

    for form in forms:
        form.to_xml(workflow)

    return etree.tostring(root, pretty_print=True)
