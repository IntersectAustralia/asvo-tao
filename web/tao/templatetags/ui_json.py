from django.conf import settings
from django.core import serializers
from django.template import Library
from tao import models
from tao.ui_modules import UIModulesHolder
from tao.xml_util import xml_parse
import json
# from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def metadata_json():
    strs = []
    for DBClass in [models.Simulation,
                    models.DataSetProperty,
                    models.BandPassFilter,
                    models.DustModel,
                    models.DataSet,
                    models.GalaxyModel,
                    models.Snapshot,
                    models.StellarModel,
                    models.GlobalParameter]:
        strs.append('"%s": %s' % (DBClass.__name__ , 
            serializers.serialize('json', DBClass.objects.all())))
        strs.append('"SurveyPreset": %s' % presets_json())
    json_str =  '{' + ',\n'.join(strs) + '}'
    if settings.METADATA_PRETTY_PRINT:
        json_dict = json.loads(json_str)
        json_str = json.dumps(json_dict, sort_keys=True, indent=4, separators=(',', ': '))
    return json_str

def presets_json():
    json_list = []
    for preset in models.SurveyPreset.objects.all():
        json_dict = {}
        params_ui_holder = UIModulesHolder(UIModulesHolder.XML, xml_parse(preset.parameters.encode()))
        json_dict['name'] = preset.name
        json_dict['pk'] = preset.pk
        json_dict['description'] = preset.description
        # json_dict['parameters'] = params_ui_holder.to_json_dict()
        json_list.append(json_dict)
    return json.dumps(json_list)


@register.simple_tag(takes_context=True)
def current_job_json(context):
    """Answer the string encoding of the job parameters, using the same format
    as the job submission form."""
    json_dict = context['ui_holder'].to_json_dict()
    json_dict['job-description'] = context['job'].description
    json_dict['job-id'] = context['id']
    json_str = json.dumps(json_dict)
    return json_str


@register.simple_tag(takes_context=True)
def loaded_job_json(context):
    """Answer the string encoding of the job parameters, using the same format
    as the job submission form."""
    json_str = '{}'
    if context.has_key('ui_holder'):
        json_dict = context['ui_holder'].to_json_dict()
        json_str = json.dumps(json_dict)
    return json_str