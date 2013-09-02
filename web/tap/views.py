import time
from lxml import etree
from tap.parser import *
from tap.settings import *
from tap.decorators import http_auth_required, tap_job_submission_request
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, StreamingHttpResponse
from django.core.exceptions import PermissionDenied
from django.core.servers.basehttp import FileWrapper
from tao.time import timestamp
from tao import models

def tap(request):
    
    return render(request, 'tap/http_response.html', 
                  {'message': 'TAO TAP Services entry point'})

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
    data_types = dict([(i,t) for i,t in models.DataSetProperty.DATA_TYPES])
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
@tap_job_submission_request
def sync(request):
    job = createTAPjob(request)
    
    while not (job.is_completed() or job.is_error()):
        time.sleep(15)
        models.Job.objects.update()
        job = models.Job.objects.get(id=job.id)
    
    return stream_job_results(request, job)
    
@csrf_exempt
@http_auth_required
@tap_job_submission_request
def async(request):
    job = createTAPjob(request)
        
    return UWSRedirect(request, job.id)

@csrf_exempt
@http_auth_required
def job(request, id):
    job = findTAPjob(request, id)
    
    if request.method == 'DELETE':
        deleteTAPJob(job)
    
    resultsURL = "%s/%d/results" % (request.build_absolute_uri("/tap/async"), job.id)
    
    return render(request, 'tap/uws-job.xml', {'job': job, 
                                               'status': UWS_JOB_STATUS[job.status], 
                                               'resultsURL': resultsURL,
                                               'duration': execution_duration})

@csrf_exempt
@http_auth_required
def phase(request, id):
    job = findTAPjob(request, id)
    
    if 'PHASE' in request.POST and request.POST['PHASE'] == 'ABORT':
        deleteTAPJob(job, 'Aborted')
    
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
    job = findTAPjob(request, id)
    deleteTAPJob(job, 'Terminated')
    
    return render(request, 'tap/http_response.html', {'message': 'TERMINATED'})

@csrf_exempt
@http_auth_required
def destruction(request, id):
    job = findTAPjob(request, id)
    deleteTAPJob(job, 'Destructed')
    
    return render(request, 'tap/http_response.html', {'message': 'DESTRUCTED'})

@csrf_exempt
@http_auth_required
def error(request, id):
    job = findTAPjob(request, id)
    
    return render(request, 'tap/error.xml', {'error': job.error_message, 
                                             'timestamp': job.created_time})

@csrf_exempt
@http_auth_required
def params(request, id):
    job = findTAPjob(request, id)
    
    return render(request, 'tap/http_response.html', {'message': job.parameters})

@csrf_exempt
@http_auth_required
def results(request, id):
    job = findTAPjob(request, id)
    
    job_file = None
    for file in job.files():
        if file.file_name[0:len(TAP_OUTPUT_PREFIX)] == TAP_OUTPUT_PREFIX:
            job_file = file
    
    if (not job_file) or (not job_file.can_be_downloaded()):
        return HttpResponseBadRequest('File not found')
    
    return render(request, 'tap/results.xml', 
                  {'download_link': "%s/%s/results/result/%s" % 
                   (request.build_absolute_uri("/tap/async"), 
                   str(id), job_file.file_name)})

@csrf_exempt
@http_auth_required
def result(request, id, file=None):
    job = findTAPjob(request, id)
    
    return stream_job_results(request, job)

@csrf_exempt
@http_auth_required
def owner(request, id):
    job = findTAPjob(request, id)
    
    return render(request, 'tap/http_response.html', {'message': job.username})

@csrf_exempt
@http_auth_required
def executionduration(request, id):
    job = findTAPjob(request, id)
    
    return render(request, 'tap/http_response.html', {'message': EXECUTION_DURATION})

def make_parameters_xml(request):
    query = prepare_query(request.POST['QUERY'])
    
    dataset    = parse_dataset_name(query)
    fields     = parse_fields(query, dataset)
    order      = parse_order(query)
    limit      = parse_limit(query)
    if ('MAXREC' in request.POST) and (request.POST['MAXREC'] != ''):
        limit  = request.POST['MAXREC']
    conditions = parse_conditions(query)
    
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
    query_node.text = query.replace(dataset['name'], '-table-')
    
    simulation_node = etree.SubElement(sql, 'simulation')
    simulation_node.text = dataset['simulation']
    
    galaxy_model_node = etree.SubElement(sql, 'galaxy-model')
    galaxy_model_node.text = dataset['galaxy_model']
    
    limit_node = etree.SubElement(sql, 'limit')
    limit_node.text = limit
    
    module_version_node = etree.SubElement(sql, 'module-version')
    module_version_node.text = str(TAP_MODULE_VERSION)
    
    votable = etree.SubElement(workflow, 'votable')
    votable.set('id', '2')
    
    field_items = etree.SubElement(votable, 'fields')
    for field in fields:
        item = etree.SubElement(field_items, 'item')
        item.set('label', field['label'])
        item.set('units', field['units'])
        item.text = field['value']
    
    parents = etree.SubElement(votable, 'parents')
    item = etree.SubElement(parents, 'item')
    item.text = '1'
    
    votable_module_version_node = etree.SubElement(votable, 'module-version')
    votable_module_version_node.text = str(TAP_MODULE_VERSION)
    
    filename_node = etree.SubElement(votable, 'filename')
    filename_node.text = TAP_OUTPUT_PREFIX + "." + TAP_OUTPUT_EXT
    
    return etree.tostring(params_xml, pretty_print=True, encoding='utf-8', 
                          xml_declaration=True)
    
def UWSRedirect(request, id, redirect=''):
    response = HttpResponse(status=303)
    response["Location"] = "%s/%s%s" % (request.build_absolute_uri("/tap/async"), 
                                        str(id), redirect)
    return response

def stream_job_results(request, job):
    if job.is_error():
        return render(request, 'tap/error.xml', {'error': job.error_message, 'timestamp': 
                                                 job.created_time, 'query': request.POST['QUERY']})
    job_file = None
    for file in job.files():
        if file.file_name[0:len(TAP_OUTPUT_PREFIX)] == TAP_OUTPUT_PREFIX:
            job_file = file
        
    if (not job_file) or (not job_file.can_be_downloaded()):
        job.error_message += "Can't get the job file.\n"
        job.save()
        return HttpResponseBadRequest('File not found')

    response = StreamingHttpResponse(streaming_content=FileWrapper(open(job_file.file_path)), 
                                     mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file.file_name
    
    return response

def createTAPjob(request):
    parameters = make_parameters_xml(request)
    
    job = models.Job(user=request.user, parameters=parameters)
    
    errors = check_query(request.POST['QUERY'])
    if errors != '':
        job.error_message = errors
        job.status = models.Job.ERROR
    else:
        dataset = parse_dataset_name(request.POST['QUERY'])
        job.database = dataset['name']
        
    job.save()
    
    return job
    
def findTAPjob(request, id):
    try:
        job = models.Job.objects.get(id=id)
    except models.Job.DoesNotExist:
        raise PermissionDenied
    
    if not job.can_read_job(request.user):
        raise PermissionDenied
    
    return job
    
def deleteTAPJob(job, action='Deleted'):
    job_stop_command = models.WorkflowCommand(job_id=job, command='Job_Stop', 
                                              submitted_by=job.user, execution_status='SUBMITTED')
    job_stop_command.save()
    job.status = models.Job.ERROR
    job.error_message = "%s by user" % action
    job.save()
    
    