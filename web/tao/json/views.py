from django.core import serializers
from django.utils import simplejson
from django.http import HttpResponse

from tao.models import Snapshot, Simulation, GalaxyModel, DataSet
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
    str = serializers.serialize('json', objects)
    return HttpResponse(str, mimetype="application/json")

@researcher_required
def simulation(request, id):
    str = '{}'
    try:
        object = Simulation.objects.get(id = id)
        str = serializers.serialize('json', [object])[1:-1]
    except Simulation.DoesNotExist:
        pass
    return HttpResponse(str, mimetype="application/json")

@researcher_required
def galaxy_model(request, id):
    str = '{}'
    try:
        object = GalaxyModel.objects.get(id = id)
        str = serializers.serialize('json', [object])[1:-1]
    except GalaxyModel.DoesNotExist:
        pass
    return HttpResponse(str, mimetype="application/json")

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
    str = simplejson.dumps(dicts)
    return HttpResponse(str, mimetype="application/json")

@researcher_required
def filters(request, sid, gid):
    """
    returns filters for given simulation and galaxy_model
    :param request:
    :param sid: simulation id
    :param gid: galaxy model id
    :return: HttpResponse in json format
    """
    data_set = DataSet.objects.get(simulation_id=sid, galaxy_model_id=gid)
    objects = datasets.filter_choices(data_set.id)
    str = serializers.serialize('json', objects)
    return HttpResponse(str, mimetype="application/json")

@researcher_required
def output_choices(request, id):
    """
    returns output choices for given dataset id
    :param request:
    :param id: data set id
    :return: HttpResponse in json format
    """
    objects = datasets.output_choices(id)
    str = serializers.serialize('json', objects)
    return HttpResponse(str, mimetype="application/json")


def bad_request(request):
    """
    returns an error to the browser
    :param request:
    :return:
    """
    return HttpResponse("{'error':'wrong api request'}", mimetype="application/json")