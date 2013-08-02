from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.servers.basehttp import FileWrapper # TODO use sendfile
from django.http import StreamingHttpResponse, Http404, HttpResponse
from django.shortcuts import render
from django.template import loader, Context
from django.utils.html import format_html

from tao.datasets import dataset_get
from tao.decorators import researcher_required, set_tab, \
    object_permission_required
from tao.models import Job, Snapshot, DataSetProperty, StellarModel, BandPassFilter, DustModel
from tao.ui_modules import UIModulesHolder
from tao.xml_util import xml_parse

import os
import zipstream

@researcher_required
@object_permission_required('can_read_job')
@set_tab('jobs')
def view_job(request, id):
    job = Job.objects.get(id=id)

    # xml_string = job.parameters
    ui_holder = UIModulesHolder(UIModulesHolder.XML, xml_parse(job.parameters.encode('utf-8')))
    forms = ui_holder.forms()

    return render(request, 'jobs/view.html', {
        'job': job,
        'forms': forms,
        'forms_size' : len(forms)+1,
    })

@researcher_required
@object_permission_required('can_read_job')
def get_file(request, id, file_path):
    job = Job.objects.get(pk=id)

    the_one = [file for file in job.files() if file.file_name == file_path]
    if len(the_one) == 0:
        raise Http404
    
    job_file = the_one[0]
    if not job_file.can_be_downloaded():
        raise PermissionDenied

    response = StreamingHttpResponse(streaming_content=FileWrapper(open(job_file.file_path)))

    # TODO sanitise filename
    response['Content-Disposition'] = 'attachment; filename="%s"' % job_file.file_name.replace('/','_')
    return response

class TaoZipPath(zipstream.ZipPath):
    def __init__(self, file_path, dir_iter = None):
        self._file_path = file_path
        self._dir_iter = dir_iter
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
        return self._file_path

@researcher_required
@object_permission_required('can_read_job')
def get_zip_file(request, id):
    job = Job.objects.get(pk=id)

    # generator mapping data from files_tree into TaoZipPath
    def to_tao_zip_path(dir_iterator):
        for fn, iter in dir_iterator:
            if iter is None:
                yield TaoZipPath(fn)
            else:
                yield TaoZipPath(fn, to_tao_zip_path(iter))

    archive = zipstream.ZipStream(to_tao_zip_path(job.files_tree()))
    response = StreamingHttpResponse(streaming_content=archive, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="tao_output.zip"'
    return response


@researcher_required
@object_permission_required('can_read_job')
def get_summary_txt_file(request, id):
    def format_redshit(redshift):
        whole_digits = int(redshift)
        return round(redshift, max(5-whole_digits, 0))

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

    job = Job.objects.get(id=id)
    ui_holder = UIModulesHolder(UIModulesHolder.XML, xml_parse(job.parameters.encode('utf-8')))

    geometry = ui_holder.raw_data('light_cone', 'catalogue_geometry')
    dataset_id = ui_holder.raw_data('light_cone', 'galaxy_model')
    output_properties = [DataSetProperty.objects.get(id=output_property_id) for output_property_id in ui_holder.raw_data('light_cone', 'output_properties')]
    output_format = ''
    for x in settings.OUTPUT_FORMATS:
        if x['value'] == (ui_holder.raw_data('output_format', 'supported_formats')):
            output_format = x['text']

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="summary.txt"'
    txt_template = loader.get_template('jobs/summary.txt')
    context = Context({
        'catalogue_geometry': geometry,
        'simulation': dataset_get(dataset_id).simulation,
        'galaxy_model': dataset_get(dataset_id).galaxy_model,
        'output_properties': output_properties,
        'record_filter': display_selection(ui_holder.raw_data('record_filter', 'filter'), ui_holder.raw_data('record_filter', 'min'), ui_holder.raw_data('record_filter', 'max')),
        'output_format': output_format,
    })
    if geometry == 'light-cone':
        ra_opening_angle = ui_holder.raw_data('light_cone', 'ra_opening_angle')
        dec_opening_angle = ui_holder.raw_data('light_cone', 'dec_opening_angle')
        redshift_min = ui_holder.raw_data('light_cone', 'redshift_min')
        redshift_max = ui_holder.raw_data('light_cone', 'redshift_max')
        context['ra_opening_angle'] = ra_opening_angle + u'\xb0'
        context['dec_opening_angle'] = dec_opening_angle + u'\xb0'
        context['redshift'] = redshift_min + ' ' + u'\u2264' + ' z ' + u'\u2264' + ' ' + redshift_max
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
        context['single_stellar_population_model'] = single_stellar_population_model
        context['band_pass_filters'] = [get_bandpass_filter(band_pass_id) for band_pass_id in band_pass_ids]
        if ui_holder.raw_data('sed', 'apply_dust'):
            context['dust_model'] = DustModel.objects.get(id=ui_holder.raw_data('sed', 'select_dust_model'))
        else:
            context['dust_model'] = 'None'

    else:
        context['apply_sed'] = False
    if ui_holder.raw_data('mock_image', 'apply_mock_image'):
        context['number_of_images'] = ui_holder.raw_data('mock_image', 'TOTAL_FORMS')
    else:
        context['number_of_images'] = None
    response.write(txt_template.render(context))
    return response


@researcher_required
@set_tab('jobs')
def index(request):
    user_jobs = Job.objects.filter(user=request.user).order_by('-id')
    return render(request, 'jobs/index.html', {
        'jobs': user_jobs,
    })