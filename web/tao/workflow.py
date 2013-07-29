"""
==================
tao.workflow
==================

Helper that saves a job from form data (in UI Holder). See :class:`tao.ui_modules.UIModulesHolder`
"""



from tao import models, time
from tao.datasets import dataset_get
from tao.xml_util import create_root, find_or_create, child_element, xml_print


def save(user, ui_holder, description=None):
    dataset = dataset_get(ui_holder.cleaned_data('light_cone', 'galaxy_model'))
    if description:
        job = models.Job(user=user, parameters=_make_parameters(user, ui_holder.forms()), database=dataset.database, description=description)
    else:
        job = models.Job(user=user, parameters=_make_parameters(user, ui_holder.forms()), database=dataset.database)
    job.save()
    return job

def _make_parameters(user, forms):
    # precondition: forms are valid

    root = create_root('tao', xmlns='http://tao.asvo.org.au/schema/module-parameters-v1', timestamp=time.timestamp())

    child_element(root, 'username', text=user.username)

    workflow = find_or_create(root, 'workflow', name='alpha-light-cone-image')
    child_element(workflow, 'schema-version', text='2.0')

    for form in forms:
        form.to_xml(workflow)

    child_element(root, 'signature', text='base64encodedsignature')

    return xml_print(root)
