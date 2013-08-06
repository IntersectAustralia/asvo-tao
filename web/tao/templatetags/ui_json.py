from django.core import serializers
from django.template import Library
from tao import models
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
    json_string =  '{' + ',\n'.join(strs) + '}'
    json_dict = json.loads(json_string)
    return json.dumps(json_dict, sort_keys=True, indent=4, separators=(',', ': '))
