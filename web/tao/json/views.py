from django.core import serializers
from django.utils import simplejson
from django.http import HttpResponse

from tao.models import Snapshot, Simulation, GalaxyModel, DataSet, DustModel, DataSetProperty, BandPassFilter, StellarModel, GlobalParameter
from tao import datasets
from tao.decorators import researcher_required


@researcher_required
def snapshots(request, sid, gid):
    """
    returns snapshots associated with dataset of given simulation and galaxy model
    :param request:
    :param sid: simulation id
    :param gid: galaxy model id
    :return:
    """
    data_set = DataSet.objects.get(simulation_id=sid, galaxy_model_id=gid)
    objects = Snapshot.objects.filter(dataset_id = data_set.id).order_by('redshift')
    resp = serializers.serialize('json', objects)
    return HttpResponse(resp, mimetype="application/json")

@researcher_required
def simulation(request, id):
    resp = '{}'
    try:
        object = Simulation.objects.get(id = id)
        resp = serializers.serialize('json', [object])[1:-1]
    except Simulation.DoesNotExist:
        pass
    return HttpResponse(resp, mimetype="application/json")

@researcher_required
def galaxy_model(request, id):
    resp = '{}'
    try:
        object = GalaxyModel.objects.get(id = id)
        resp = serializers.serialize('json', [object])[1:-1]
    except GalaxyModel.DoesNotExist:
        pass
    return HttpResponse(resp, mimetype="application/json")

@researcher_required
def galaxy_models(request, id):
    """
    returns a dict with dataset info for a given simulation according to available datasets
    :param request: HttpRequest
    :param id: simulation_id
    :return: HttpResponse in json format
    """
    data_sets = DataSet.objects.filter(simulation_id = id).select_related('galaxy_model').order_by('galaxy_model__name')
    dicts = [{'id':x.id, 'name':x.galaxy_model.name, 'galaxy_model_id':x.galaxy_model_id} for x in data_sets]
    resp = simplejson.dumps(dicts)
    return HttpResponse(resp, mimetype="application/json")

@researcher_required
def filters(request, id):
    """
    returns filters for given simulation and galaxy_model
    :param request:
    :param id: data set id
    :return: HttpResponse in json format
    """
    def json_my_encode(obj, extension=None):
        if isinstance(obj, DataSetProperty):
            return {'type':'D','pk':obj.pk, 'fields':{'name':obj.name,'units':obj.units,'label':obj.label,'data_type':obj.data_type}}
        elif isinstance(obj, BandPassFilter):
            return {'type':'B','pk':str(obj.pk) + '_' + extension, 'fields':{'name':obj.filter_id,'units':'','label':obj.label + ' (' + extension.capitalize() + ')','data_type':DataSetProperty.TYPE_FLOAT}}
        else:
            raise TypeError(repr(obj) + " is not JSON serializable by our custom method")
    def gen_pairs(objs):
        for obj in objs:
            yield json_my_encode(obj, 'apparent')
            yield json_my_encode(obj, 'absolute')
    data_set = DataSet.objects.get(pk=id)
    objects = datasets.filter_choices(id)
    default_filter = data_set.default_filter_field
    if default_filter is None:
        default_id = ''
    else:
        default_id = str(default_filter.id)
    resp = {'list': [], 'default_id':default_id, 'default_min':data_set.default_filter_min, 'default_max':data_set.default_filter_max}
    resp = simplejson.dumps(resp)
    filters = [json_my_encode(object) for object in objects]
    bandpass = [custom_dict for custom_dict in gen_pairs(datasets.band_pass_filters_objects())]
    resp = resp.replace('[]', simplejson.dumps(filters + bandpass))
    return HttpResponse(resp, mimetype="application/json")

@researcher_required
def output_choices(request, id):
    """
    returns output choices for given dataset id
    :param request:
    :param id: data set id
    :return: HttpResponse in json format
    """
    objects = datasets.output_choices(id)
    resp = serializers.serialize('json', objects)
    return HttpResponse(resp, mimetype="application/json")

@researcher_required
def stellar_model(request, id):
    resp = '{}'
    try:
        object = StellarModel.objects.get(id = id)
        resp = serializers.serialize('json', [object])[1:-1]
    except StellarModel.DoesNotExist:
        pass
    return HttpResponse(resp, mimetype="application/json")

@researcher_required
def dust_model(request, id):
    resp = '{}'
    try:
        object = DustModel.objects.get(id = id)
        resp = serializers.serialize('json', [object])[1:-1]
    except DustModel.DoesNotExist:
        pass
    return HttpResponse(resp, mimetype="application/json")

@researcher_required
def global_parameter(request, parameter_name):
    resp = '{}'
    try:
        object = GlobalParameter.objects.get(parameter_name = parameter_name)
        resp = serializers.serialize('json', [object])[1:-1]
    except GlobalParameter.DoesNotExist:
        pass
    return HttpResponse(resp, mimetype="application/json")

@researcher_required
def bandpass_filters(request):
    def gen_json(obj, extension):
        return '{"pk": "' + str(obj.id) + '_' + extension + '", "model": "tao.bandpassfilter", "fields": {"order": ' + str(obj.order) + ', "filter_id": "' + obj.filter_id + '", "group": "' + obj.group + '", "description": "' + obj.description + '", "label": "' + obj.label + ' (' + extension.capitalize() + ')"}}'
    def gen_pairs(objs):
        for obj in objs:
            yield gen_json(obj, 'apparent')
            yield gen_json(obj, 'absolute')
    objects = BandPassFilter.objects.all()
    resp = '[' + ','.join([json_str for json_str in gen_pairs(objects)]) + ']'
    return HttpResponse(resp, mimetype="application/json")

def bad_request(request):
    """
    returns an error to the browser
    :param request:
    :return:
    """
    return HttpResponse("{'error':'wrong api request'}", mimetype="application/json")

