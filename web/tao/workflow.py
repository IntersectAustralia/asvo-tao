"""
    module responsible for constructing the parameters
"""

from tao.xml_util import create_root, find_or_create, child_element, xml_print

from tao import models, time

from decimal import Decimal

def save(user, forms):
    job = models.Job(user=user, parameters=_make_parameters(user, forms))
    job.save()
    return job

def _make_parameters(user, forms):
    # precondition: forms are valid

    root = create_root('tao', xmlns='http://tao.asvo.org.au/schema/module-parameters-v1', timestamp=time.timestamp())

    child_element(root, 'username', text=user)

    workflow = find_or_create(root, 'workflow', name='alpha-light-cone-image')
    child_element(workflow, 'schema-version', text='1.0')

    for form in forms:
        form.to_xml(workflow)

    child_element(root, 'signature', text='base64encodedsignature')

    return xml_print(root)
