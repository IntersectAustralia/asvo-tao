from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.servers.basehttp import FileWrapper # TODO use sendfile
from django.core.urlresolvers import reverse
from django.http import StreamingHttpResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.template import loader, Context, RequestContext
from django.views.decorators.csrf import csrf_exempt

from tao.datasets import dataset_get
from tao.decorators import researcher_required, set_tab, \
    object_permission_required
from tao.models import Job, Snapshot, DataSetProperty, StellarModel, BandPassFilter, DustModel, WorkflowCommand,GlobalParameter
from tao.ui_modules import UIModulesHolder
from tao.xml_util import xml_parse
from tao.utils import output_formats

from tap.decorators import http_auth, access_job

import os, StringIO, subprocess
import zipstream, html2text

@researcher_required
@object_permission_required('can_read_job')
@set_tab('jobs')
def view_job(request, id):
    job = Job.objects.get(id=id)

    # xml_string = job.parameters
    ui_holder = UIModulesHolder(UIModulesHolder.XML, xml_parse(job.parameters.encode('utf-8')))
    forms = ui_holder.forms()
    
    return render(request, 'jobs/view.html', {
        'id': id,
        'user': request.user,
        'job': job,
        'ui_holder': ui_holder,
        'forms': forms,
        'forms_size': len(forms)+1,
    })

@researcher_required
@object_permission_required('can_read_job')
def get_file(request, id, file_path):
    job = Job.objects.get(pk=id)

    the_one = [file for file in job.files() if file.file_name == file_path]
    if len(the_one) == 0:
        raise Http404
    
    job_file = the_one[0]

    response = StreamingHttpResponse(streaming_content=FileWrapper(open(job_file.file_path)), mimetype='application/force-download')

    # TODO sanitise filename
    response['Content-Disposition'] = 'attachment; filename="%s"' % job_file.file_name.replace('/','_')
    return response

class TaoZipPath(zipstream.ZipPath):
    def __init__(self, file_path, dir_iter = None, file_info = None):
        self._file_path = file_path
        self._dir_iter = dir_iter
        self._file_info = file_info
        self._basename = os.path.basename(file_path)

    def basename(self):
        """
        Returns the basename of this ZipPath instance
        """
        return self._basename.encode("utf8")

    def isdir(self):
        """
        Returns true if this ZipPath instance represents a directory
        """
        return self._dir_iter is not None

    def listdir(self):
        """
        If self.isdir(), this should be an iterator of ZipPath instances inside
        """
        return self._dir_iter

    def file(self):
        """
        If not self.isdir(), this should return a filename to open
        """
        if self._file_info:
            return self._file_info
        else:
            return self._file_path


def _get_summary_as_text(id):
    def get_bandpass_filter(bp_filter_id):
        suffix = ''
        if bp_filter_id.endswith('_apparent'):
            bp_filter_id = bp_filter_id[:-len('apparent')-1]
            suffix = 'apparent'
        elif bp_filter_id.endswith('_absolute'):
            bp_filter_id = bp_filter_id[:-len('absolute')-1]
            suffix = 'absolute'
        obj = BandPassFilter.objects.get(id=bp_filter_id)
        return obj.label + ' (' + suffix.capitalize() + ')'

    def format_redshit(redshift):
        whole_digits = int(redshift)
        return round(redshift, max(5-whole_digits, 0))

    def display_range(label, min, max):
        if max is not None and min is not None:
            return min + ' ' + u'\u2264' + ' ' + label + ' ' + u'\u2264' + ' ' + max
        elif max is None:
            return min + ' ' + u'\u2264' + ' ' + label
        else:
            return label + ' ' + u'\u2264' + ' ' + max

    def display_selection(filter_id, min, max):
        if filter_id.startswith('D-'):
            filter_id = filter_id[2:]
            obj = DataSetProperty.objects.get(id=filter_id)
            return display_range(obj.label + ' (' + obj.units + ')', min, max)
        elif filter_id.startswith('B-'): # bandpass filter_id looks like B-12_apparent
            filter_id = filter_id[2:]
            filter_label = get_bandpass_filter(filter_id)
            return display_range(filter_label, min, max)
        else:
            return 'No Filter'

    job = Job.objects.get(pk=id)
    ui_holder = UIModulesHolder(UIModulesHolder.XML, xml_parse(job.parameters.encode('utf-8')))
    TAO_acknowledgement= html2text.html2text(GlobalParameter.objects.get(parameter_name='tao_acknowledgement').parameter_value)
    if ui_holder.job_type == UIModulesHolder.SQL_JOB:
        txt_template = loader.get_template('jobs/sql_job-summary.txt')
        query = ui_holder.raw_data('sql_job', 'query')
        dataset = ui_holder.dataset
        simulation = dataset.simulation
        galaxy_model = dataset.galaxy_model
        
        output_properties = []
        for output_property in ui_holder.raw_data('sql_job', 'output_properties'):
            output_properties = output_properties + [(output_property['label'], output_property['units'])]
        output_format = ''
        for x in output_formats():
            if x['value'] == (ui_holder.raw_data('output_format', 'supported_formats')):
                output_format = x['text']
        context = Context({
            'TAO_acknowledgement':html2text.html2text(TAO_acknowledgement),        
            'query': query,
            'dark_matter_simulation': simulation,
            'simulation_details': html2text.html2text(simulation.details),
            'galaxy_model': galaxy_model,
            'galaxy_model_details': html2text.html2text(galaxy_model.details),
            'output_properties': output_properties,
            'simulation_acknowledgement': html2text.html2text(simulation.acknowledgement_txt),
            'galaxy_model_acknowledgement': html2text.html2text(galaxy_model.acknowledgement_txt),
            'output_format': output_format,})
    else:
        geometry = ui_holder.raw_data('light_cone', 'catalogue_geometry')
        dataset = ui_holder.dataset
        simulation = dataset.simulation
        galaxy_model = dataset.galaxy_model
        output_properties = []
        for output_property_id in ui_holder.raw_data('light_cone', 'output_properties'):
            output_property = DataSetProperty.objects.get(id=output_property_id)
            units = html2text.html2text(output_property.units).rstrip()
            output_properties = output_properties + [(output_property, units)]
        # output_properties = [(DataSetProperty.objects.get(id=output_property_id), html2text.html2text(getattr(DataSetProperty.objects.get(id=output_property_id), 'units')).rstrip()) for output_property_id in ui_holder.raw_data('light_cone', 'output_properties')]
        output_format = ''
        for x in output_formats():
            if x['value'] == (ui_holder.raw_data('output_format', 'supported_formats')):
                output_format = x['text']

        txt_template = loader.get_template('jobs/light_cone_job-summary.txt')
        context = Context({
            'TAO_acknowledgement':html2text.html2text(TAO_acknowledgement),
            'catalogue_geometry': geometry,
            'dark_matter_simulation': simulation,
            'simulation_details': html2text.html2text(simulation.details),
            'simulation_acknowledgement': html2text.html2text(simulation.acknowledgement_txt),
            'galaxy_model': galaxy_model,
            'galaxy_model_details': html2text.html2text(galaxy_model.details),
            'galaxy_model_acknowledgement': html2text.html2text(galaxy_model.acknowledgement_txt),
            'output_properties': output_properties,
            'record_filter': display_selection(ui_holder.raw_data('record_filter', 'filter'), ui_holder.raw_data('record_filter', 'min'), ui_holder.raw_data('record_filter', 'max')),
            'output_format': output_format,
        })
        if geometry == 'light-cone':
            ra_min_angle = ui_holder.raw_data('light_cone', 'ra_min')
            dec_min_angle = ui_holder.raw_data('light_cone', 'dec_min')
            ra_max_angle = ui_holder.raw_data('light_cone', 'ra_max')
            dec_max_angle = ui_holder.raw_data('light_cone', 'dec_max')
            context['ra_min_angle'] = ra_min_angle
            context['dec_min_angle'] = dec_min_angle
            context['ra_max_angle'] = ra_max_angle
            context['dec_max_angle'] = dec_max_angle
            
            context['redshift_min'] = ui_holder.raw_data('light_cone', 'redshift_min')
            context['redshift_max'] = ui_holder.raw_data('light_cone', 'redshift_max')
            context['number_of_light_cones'] = ui_holder.raw_data('light_cone', 'number_of_light_cones')
            context['light_cone_type'] = ui_holder.raw_data('light_cone', 'light_cone_type')
        else:
            snapshot = Snapshot.objects.get(id=ui_holder.raw_data('light_cone', 'snapshot')).redshift
            context['box_size'] = ui_holder.raw_data('light_cone', 'box_size')
            context['snapshot'] = format_redshit(snapshot)

        if ui_holder.raw_data('sed', 'apply_sed'):
            single_stellar_population_model = StellarModel.objects.get(id=ui_holder.raw_data('sed', 'single_stellar_population_model'))
            band_pass_ids = ui_holder.raw_data('sed', 'band_pass_filters')
            context['apply_sed'] = True
            context['ssp_name'] = single_stellar_population_model
            context['ssp_description'] = html2text.html2text(single_stellar_population_model.description)
            context['band_pass_filters'] = [get_bandpass_filter(band_pass_id) for band_pass_id in band_pass_ids]
            if ui_holder.raw_data('sed', 'apply_dust'):
                dust_model = DustModel.objects.get(id=ui_holder.raw_data('sed', 'select_dust_model'))
                context['dust_label'] = dust_model
                context['dust_model_details'] = html2text.html2text(dust_model.details)
            else:
                context['dust_label'] = 'None'

        else:
            context['apply_sed'] = False
        if ui_holder.raw_data('mock_image', 'apply_mock_image'):
            context['number_of_images'] = ui_holder.raw_data('mock_image', 'TOTAL_FORMS')
            images = []
            for i in xrange(0, context['number_of_images']):
                image = {} 
                image['fov_dec'] = ui_holder.raw_data('mock_image', '%d-fov_dec' % i)
                image['sub_cone'] = ui_holder.raw_data('mock_image', '%d-sub_cone' % i)
                image['height'] = ui_holder.raw_data('mock_image', '%d-height' % i)
                image['origin_ra'] = ui_holder.raw_data('mock_image', '%d-origin_ra' % i)
                image['min_mag'] = ui_holder.raw_data('mock_image', '%d-min_mag' % i)
                image['origin_dec'] = ui_holder.raw_data('mock_image', '%d-origin_dec' % i)
                image['width'] = ui_holder.raw_data('mock_image', '%d-width' % i)
                image['z_min'] = ui_holder.raw_data('mock_image', '%d-z_min' % i)
                image['max_mag'] = ui_holder.raw_data('mock_image', '%d-max_mag' % i)
                image['z_max'] = ui_holder.raw_data('mock_image', '%d-z_max' % i)
                image['fov_ra'] = ui_holder.raw_data('mock_image', '%d-fov_ra' % i)
                image['format'] = ui_holder.raw_data('mock_image', '%d-format' % i)
                mag_fields = ui_holder.raw_data('mock_image','%d-mag_field' % i).split('_')
                mag_field = BandPassFilter.objects.get(pk=mag_fields[0]).label
                mag_field += ' (%s)' % mag_fields[1].title()
                image['mag_field'] = mag_field
                images.append(image)
            context['images'] = images
        else:
            context['number_of_images'] = None
    return txt_template.render(context)

@researcher_required
@object_permission_required('can_read_job')
def get_zip_file(request, id):
    job = Job.objects.get(pk=id)
    summary_blob = _get_summary_as_text(id).encode('utf8')
    summary_io = StringIO.StringIO(summary_blob)

    # generator mapping data from files_tree into TaoZipPath
    def to_tao_zip_path(dir_iterator, top=False):
        for fn, iter in dir_iterator:
            if iter is None:
                yield TaoZipPath(fn)
            else:
                yield TaoZipPath(fn, to_tao_zip_path(iter))
        if top:
            yield TaoZipPath('summary.txt', None, {'stream': summary_io, 'size': len(summary_blob)})

    archive = zipstream.ZipStream(to_tao_zip_path(job.files_tree(), True))
    filename = 'tao_%s_catalogue_%d.zip' % (job.user.username, job.id)
    response = StreamingHttpResponse(streaming_content=archive, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename,)
    return response

def stream_from_pipe(command):
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    content = None
    while content != '':
        content = pipe.stdout.read(1024)
        yield content
    
def summary_temp_location(job):
    tmp_dir      = os.path.dirname(settings.SUMMARY_TMP)
    job_tmp_dir  = os.path.join(tmp_dir, str(job.id))
    summary_path = os.path.join(job_tmp_dir, 'summary.txt')
    
    if not os.path.isfile(summary_path):
        mode = 0700
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)
            os.chmod(tmp_dir, mode)
        if not os.path.isdir(job_tmp_dir):
            os.mkdir(job_tmp_dir)
            os.chmod(job_tmp_dir, mode)
            
        summary_text = _get_summary_as_text(job.id).encode('utf8')
        f = open(summary_path, "w")
        f.write(summary_text)
        f.close()
    
    return job_tmp_dir

@researcher_required
@object_permission_required('can_read_job')
def get_tar_file(request, id):
    return _get_tar_file(request, id)


def _get_tar_file(request, id):
    job = Job.objects.get(pk=id)
    summary_dir = summary_temp_location(job)
    output_path = os.path.dirname(os.path.join(settings.FILES_BASE, job.output_path, 'output'))
    tar_command = ['tar', '-cf', '-', '-C', output_path, '.', '-C', summary_dir, '.']
    response = StreamingHttpResponse(streaming_content=stream_from_pipe(tar_command), 
                                     content_type='application/x-tar')
    response['Content-Disposition'] = 'attachment; filename="tao_%s_catalogue_%d.tar"' % (job.username(), job.id)
    return response

@csrf_exempt
@http_auth
def basic_tar_file(request, id):
    "Allow download with basic auth"
    return _get_tar_file(request, id)


@researcher_required
@object_permission_required('can_read_job')
def get_summary_txt_file(request, id):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="summary.txt"'
    response.write(_get_summary_as_text(id))
    return response

STATUS_ORDERING = {
    'HELD': 0,
    'SUBMITTED': 1,
    'QUEUED': 2,
    'IN_PROGRESS': 3,
    'COMPLETED': 4,
    'ERROR': 5,
}


def _qsort_jobs(job_list):
    if not job_list:
        return []
    else:
        pivot = job_list[0]
        less = _qsort_jobs([job for job in job_list[1:] if STATUS_ORDERING[job.status] <= STATUS_ORDERING[pivot.status]]) # since first ordered by ascending id, this equality places bigger id of the same status in front
        greater = _qsort_jobs([job for job in job_list[1:] if STATUS_ORDERING[job.status] > STATUS_ORDERING[pivot.status]])
        return less + [pivot] + greater


@researcher_required
@set_tab('jobs')
def index(request):
    user_jobs = Job.objects.filter(user=request.user).order_by('-id')

    return render(request, 'jobs/index.html', {
        'jobs': user_jobs,
        'user': request.user
    })

@researcher_required
@object_permission_required('can_write_job')
def stop_job(request, id):
    job = Job.objects.get(id=id)
    job_stop_command = WorkflowCommand(job_id=job, command='Job_Stop', submitted_by=request.user, execution_status='SUBMITTED')
    job_stop_command.save()
    return HttpResponse('{}', mimetype='application/json')

@researcher_required
@object_permission_required('can_write_job')
def rerun_job(request, id):
    job = Job.objects.get(id=id)
    job.status = 'SUBMITTED'
    job.save()
    return HttpResponse('{}', mimetype='application/json')

@researcher_required
@object_permission_required('can_write_job')
def release_job(request, id):
    job = Job.objects.get(id=id)
    job.status = 'SUBMITTED'
    job.save()
    return HttpResponse('{}', mimetype='application/json')

@researcher_required
@object_permission_required('can_write_job')
def delete_job_output(request, id):
    if request.method == "POST":
        job = Job.objects.get(id=id)
        job_output_delete_command = WorkflowCommand(
                job_id=job,
                command='Job_Output_Delete',
                parameters=job.user.username,
                submitted_by=request.user,
                execution_status='SUBMITTED')
        job_output_delete_command.save()
    response = '{{"next_url":"{0}"}}'.format(reverse('job_index'))
    return HttpResponse(response, mimetype='application/json')

@researcher_required
@object_permission_required('can_write_job')
def refresh_disk_usage(request, id):
    job = Job.objects.get(id=id)
    job.recalculate_disk_usage()
    return redirect(reverse('view_job', args=[id]))
