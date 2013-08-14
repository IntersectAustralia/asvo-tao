from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.servers.basehttp import FileWrapper # TODO use sendfile
from django.http import StreamingHttpResponse, Http404, HttpResponse
from django.shortcuts import render
from django.template import loader, Context

from tao.datasets import dataset_get
from tao.decorators import researcher_required, set_tab, \
    object_permission_required
from tao.models import Job, Snapshot, DataSetProperty, StellarModel, BandPassFilter, DustModel
from tao.ui_modules import UIModulesHolder
from tao.xml_util import xml_parse

import os, StringIO
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
        'job': job,
        'ui_holder': ui_holder,
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

    geometry = ui_holder.raw_data('light_cone', 'catalogue_geometry')
    dataset_id = ui_holder.raw_data('light_cone', 'galaxy_model')
    simulation = dataset_get(dataset_id).simulation
    galaxy_model = dataset_get(dataset_id).galaxy_model
    output_properties = [DataSetProperty.objects.get(id=output_property_id) for output_property_id in ui_holder.raw_data('light_cone', 'output_properties')]
    output_format = ''
    for x in settings.OUTPUT_FORMATS:
        if x['value'] == (ui_holder.raw_data('output_format', 'supported_formats')):
            output_format = x['text']

    txt_template = loader.get_template('jobs/summary.txt')
    context = Context({
        'catalogue_geometry': geometry,
        'dark_matter_simulation': simulation,
        'simulation_details': html2text.html2text(simulation.details),
        'galaxy_model': galaxy_model,
        'galaxy_model_details': html2text.html2text(galaxy_model.details),
        'output_properties': output_properties,
        'record_filter': display_selection(ui_holder.raw_data('record_filter', 'filter'), ui_holder.raw_data('record_filter', 'min'), ui_holder.raw_data('record_filter', 'max')),
        'output_format': output_format,
    })
    if geometry == 'light-cone':
        ra_opening_angle = ui_holder.raw_data('light_cone', 'ra_opening_angle')
        dec_opening_angle = ui_holder.raw_data('light_cone', 'dec_opening_angle')
        context['ra_opening_angle'] = ra_opening_angle
        context['dec_opening_angle'] = dec_opening_angle
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
    response = StreamingHttpResponse(streaming_content=archive, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="tao_output.zip"'
    return response


@researcher_required
@object_permission_required('can_read_job')
def get_summary_txt_file(request, id):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="summary.txt"'
    response.write(_get_summary_as_text(id))
    return response


@researcher_required
@set_tab('jobs')
def index(request):
    user_jobs = Job.objects.filter(user=request.user).order_by('-id')
    return render(request, 'jobs/index.html', {
        'jobs': user_jobs,
    })