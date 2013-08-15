import time
from lxml import etree
from tap.parser import *
from tap.settings import *
from tap.decorators import http_auth_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from tao.time import timestamp
from tao import models

def tap(request):
    
    return render(request, 'tap/http_response.html', {'message': 'TAO TAP Services entry point'})

def capabilities(request):
    
    return render(request, 'tap/capabilities.xml', 
                  {'baseUrl':           request.build_absolute_uri("/tap"), 
                   'languages':         TAP_LANGUAGES,
                   'formats':           TAP_FORMATS,
                   'retentionPeriod':   TAP_RETENTION_PERIOD,
                   'executionDuration': TAP_EXECUTION_DURATION,
                   'outputLimit':       TAP_OUTPUT_LIMIT,
                   'capabilities':      TAP_CAPABILITIES})

def availability(request):
    return render(request, 'tap/availability.xml', 
                  {'available': TAP_IS_AVAILABLE, 'note': TAP_AVAILABILITY_NOTE})

def tables(request):
    available_datasets = models.DataSet.objects.filter(available=1)
    dataset_properties = []
    data_types = {i:t for i,t in models.DataSetProperty.DATA_TYPES}
    for dataset in available_datasets:
        properties = models.DataSetProperty.objects.filter(dataset_id = dataset.id, 
            is_output = True).order_by('group', 'order', 'label')
        dataset_properties.append({"name": dataset.database, "properties": properties})
    return render(request, 'tap/tables.xml', 
                  {'datasets': dataset_properties, 'data_types': data_types})

def query(request):
    
    return render(request, 'tap/query.html', {})

@csrf_exempt
@http_auth_required
def sync(request):
    
    if 'QUERY' not in request.POST:
        return HttpResponseBadRequest('Missing query')
        
    parameters = make_parameters_xml(request)
    
    job = models.Job(user=request.user, parameters=parameters)
    
    errors = check_query(request.POST['QUERY'])
    if errors != '':
        job.error_message = errors
        job.status = models.Job.ERROR
    
    job.save()
    
    while not (job.is_completed() or job.is_error()):
        time.sleep(30)
    
    return stream_job_results(request, job)
    
@csrf_exempt
@http_auth_required
def async(request):
    
    if 'QUERY' not in request.POST:
        return HttpResponseBadRequest('Missing query')
    
    parameters = make_parameters_xml(request)
    
    job = models.Job(user=request.user, parameters=parameters)
    
    errors = check_query(request.POST['QUERY'])
    if errors != '':
        job.error_message = errors
        job.status = models.Job.ERROR
    
    job.save()
        
    return UWSRedirect(request, job.id)

@csrf_exempt
@http_auth_required
def job(request, id):
    job = models.Job.objects.get(id=id)
    if job is None:
        return HttpResponseBadRequest('Wrong URL')
    
    if 'REQUEST_METHOD' in request.META and request.META['REQUEST_METHOD'] == 'DELETE':
        print 'DELETE'
    
    resultsURL = "%s/%d/results" % (request.build_absolute_uri("/tap/async"), job.id)
    return render(request, 'tap/uws-job.xml', {'job': job, 
                                               'status': UWS_JOB_STATUS[job.status], 
                                               'resultsURL': resultsURL,
                                               'duration': execution_duration})

@csrf_exempt
@http_auth_required
def phase(request, id):
    job = models.Job.objects.get(id=id)
    if job is None:
        return HttpResponseBadRequest('Wrong URL')
    
    if 'get' not in request.GET:
        return UWSRedirect(request, job.id, '/phase?get')
    else:
        return render(request, 'tap/http_response.html', 
                      {'message': UWS_JOB_STATUS[job.status]})

@csrf_exempt
@http_auth_required
def quote(request, id):
    
    return render(request, 'tap/http_response.html', {'message': id})

@csrf_exempt
@http_auth_required
def termination(request, id):
    print 'DELETE'
    return render(request, 'tap/http_response.html', {'message': 'TERMINATED'})

@csrf_exempt
@http_auth_required
def destruction(request, id):
    print 'DELETE'
    return render(request, 'tap/http_response.html', {'message': 'DESTRUCTED'})

@csrf_exempt
@http_auth_required
def error(request, id):
    job = models.Job.objects.get(id=id)
    if job is None:
        return HttpResponseBadRequest('Wrong URL')
    
    return render(request, 'tap/error.xml', {'error': job.error_message, 'timestamp': job.created_time})

@csrf_exempt
@http_auth_required
def params(request, id):
    job = models.Job.objects.get(id=id)
    if job is None:
        return HttpResponseBadRequest('Wrong URL')
    
    return render(request, 'tap/http_response.html', {'message': job.parameters})

@csrf_exempt
@http_auth_required
def results(request, id):
    job = models.Job.objects.get(id=id)
    if job is None:
        return HttpResponseBadRequest('Wrong URL')
    
    for file in job.files():
        if file.file_name == TAP_OUTPUT_FILENAME:
            job_file = file
    
    if (not job_file) or (not job_file.can_be_downloaded()):
        raise PermissionDenied
    
    return render(request, 'tap/results.xml', 
                  {'download_link': "%s/%s/results/result/%s" % (request.build_absolute_uri("/tap/async"), 
                   str(id), job_file.file_name)})

@csrf_exempt
@http_auth_required
def result(request, id, file):
    job = models.Job.objects.get(id=id)
    if job is None:
        return HttpResponseBadRequest('Wrong URL')
    
    return stream_job_results(request, job)

@csrf_exempt
@http_auth_required
def owner(request, id):
    job = models.Job.objects.get(id=id)
    if job is None:
        return HttpResponseBadRequest('Wrong URL')
    
    return render(request, 'tap/http_response.html', {'message': job.username})

@csrf_exempt
@http_auth_required
def executionduration(request, id):
    job = models.Job.objects.get(id=id)
    if job is None:
        return HttpResponseBadRequest('Wrong URL')
    
    return render(request, 'tap/http_response.html', {'message': EXECUTION_DURATION})

def make_parameters_xml(request):
    
    query = prepare_query(request.POST['QUERY'])
    
    fields = parse_fields(query)
    dataset = parse_dataset_name(query)

    params_xml = etree.Element("tao")
    params_xml.set('timestamp', timestamp())
    params_xml.set('xmlns', 'http://tao.asvo.org.au/schema/module-parameters-v1')
    
    username_node = etree.SubElement(params_xml, 'username')
    username_node.text = request.user.username
    
    workflow = etree.SubElement(params_xml, 'workflow')
    workflow.set('name', TAP_WORKFLOW)
    
    schema_version = etree.SubElement(workflow, 'schema-version')
    schema_version.text = TAP_SCHEMA_VERSION
    
    sql = etree.SubElement(workflow, 'sql')
    sql.set('id', '1')
    
    query_node = etree.SubElement(sql, 'query')
    query_node.text = query
    
    module_version_node = etree.SubElement(sql, 'module-version')
    module_version_node.text = str(TAP_MODULE_VERSION)
    
    votable = etree.SubElement(workflow, 'votable')
    votable.set('id', '2')
    
    field_items = etree.SubElement(votable, 'fields')
    for field in fields:
        item = etree.SubElement(field_items, 'item')
        item.set('lebel', field['label'])
        item.set('units', field['units'])
        item.text = field['value']
    
    parents = etree.SubElement(votable, 'parents')
    item = etree.SubElement(parents, 'item')
    item.text = '1'
    
    votable_module_version_node = etree.SubElement(votable, 'module-version')
    votable_module_version_node.text = str(TAP_MODULE_VERSION)
    
    filename_node = etree.SubElement(votable, 'filename')
    filename_node.text = TAP_OUTPUT_FILENAME
    
    return etree.tostring(params_xml, pretty_print=True, encoding='utf-8', 
                          xml_declaration=True)
    
def UWSRedirect(request, id, redirect=''):
    response = HttpResponse(status=303)
    response["Location"] = "%s/%s%s" % (request.build_absolute_uri("/tap/async"), 
                                        str(id), redirect)
    return response

def stream_job_results(request, job):
    
    if job.is_error():
        return render(request, 'tap/error.xml', {'error': job.error_message, 'timestamp': job.created_time, 'query': request.POST['QUERY']})
    
    for file in job.files():
        if file.file_name == TAP_OUTPUT_FILENAME:
            job_file = file
        
    if (not job_file) or (not job_file.can_be_downloaded()):
        raise PermissionDenied

    response = StreamingHttpResponse(streaming_content=FileWrapper(open(job_file.file_path)))
    response['Content-Disposition'] = 'attachment; filename="%s"' % job_file.file_name.replace('/','_')
    
    return response
    