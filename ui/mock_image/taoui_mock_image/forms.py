"""
========================
taoui_mock_image.forms
========================

"""

import os

from django import forms
from django.forms.formsets import formset_factory
import form_utils.fields as bf_fields
from form_utils.forms import BetterForm
from django.utils.translation import ugettext_lazy as _

from tao import datasets
from tao import models as tao_models
from tao.forms import FormsGraph
from tao.widgets import ChoiceFieldWithOtherAttrs, TwoSidedSelectWidget
from tao.xml_util import module_xpath, module_xpath_iterate

def to_xml_2(form, root):
    if form.apply_mock_image:
        from tao.xml_util import find_or_create, child_element

        # Prepare the base element.
        mi_elem = find_or_create(root, 'skymaker', id=FormsGraph.MOCK_IMAGE_ID)
        child_element(mi_elem, 'module-version', text=Form.MODULE_VERSION)
        child_element(child_element(mi_elem, 'parents'), 'item', text=FormsGraph.BANDPASS_FILTER_ID)

        # Create a list element for the images.
        list_elem = child_element(mi_elem, 'images')

        # Iterate over the forms, creating entries. Remember there will always
        # be one extra empty form, so don't include it.
        assert form.total_form_count() > 0, 'Internal error, this should never happen!'
        for ii, sub in enumerate(form):
            if ii < form.total_form_count() - 1:
                sub_elem = child_element(list_elem, 'item')
                for field, val in sub.cleaned_data.iteritems():
                    child_element(sub_elem, field, str(val))

def from_xml_2(cls, ui_holder, xml_root, prefix=None):
    mi = xml_root.xpath('//workflow/skymaker')
    apply_mock_image = mi is not None
    params = {'mock_image-apply_mock_image': apply_mock_image}
    if apply_mock_image:

        # Find the images and setup the management form.
        imgs = xml_root.xpath('//skymaker/images/item')
        params[prefix + '-TOTAL_FORMS'] = len(imgs)
        params[prefix + '-INITIAL_FORMS'] = len(imgs)
        params[prefix + '-MAX_NUM_FORMS'] = 1000

        # Process each image.
        for ii, img in enumerate(imgs):
            pre = prefix + '-' + str(ii) + '-'
            for field in img:
                params[pre + field.tag] = field.text

    # Create the class.
    return cls(ui_holder, params, prefix=prefix)

class SingleForm(BetterForm):

    FORMAT_CHOICES = [
        ('FITS', 'FITS'),
        ('PNG', 'PNG'),
        ('JPEG', 'JPEG')
    ]

    SUB_CONE_CHOICES = [
        ('ALL', 'ALL'),
    ] + [(str(ii), str(ii)) for ii in xrange(20)]

    def __init__(self, *args, **kwargs):
        super(SingleForm, self).__init__(*args, **kwargs)

        self.fields['sub_cone'] = forms.ChoiceField(label=_('Sub-cone index:'), choices=self.SUB_CONE_CHOICES, required=True)
        self.fields['format'] = forms.ChoiceField(label=_('Output format:'), choices=self.FORMAT_CHOICES,
                                                  required=True)
        self.fields['mag_field'] = forms.ChoiceField(label=_('Magnitude field:'),
                                                     choices=datasets.band_pass_filters_enriched(), required=True)
        self.fields['min_mag'] = forms.DecimalField(label=_('Minimum magnitude:'), required=True)
        self.fields['z_min'] = forms.DecimalField(label=_('Minimum redshift:'), required=True)
        self.fields['z_max'] = forms.DecimalField(label=_('Maximum redshift:'), required=True)
        self.fields['origin_ra'] = forms.DecimalField(label=_('Center on RA:'), required=True)
        self.fields['origin_dec'] = forms.DecimalField(label=_('Center on DEC:'), required=True)
        self.fields['fov_ra'] = forms.DecimalField(label=_('FOV range RA:'), required=True)
        self.fields['fov_dec'] = forms.DecimalField(label=_('FOV range DEC:'), required=True)
        self.fields['width'] = forms.IntegerField(label=_('Image width in pixels:'), required=True)
        self.fields['height'] = forms.IntegerField(label=_('Image height in pixels:'), required=True)

    def full_clean(self):

        # Update the choices before continuing.
        self.fields['sub_cone'].choices.append(('ALL', 'ALL'))
        self.fields['mag_field'].choices.append(('test', 'test')) # TODO: Remove.

        return super(SingleForm, self).full_clean()

# Define a formset.
BaseForm = formset_factory(SingleForm, extra=1)

class Form(BaseForm):
    EDIT_TEMPLATE = 'taoui_mock_image/edit.html'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'taoui_mock_image/summary.html'
    LABEL = 'Mock Image'

    def __init__(self, *args, **kwargs):
        self.ui_holder = args[0]

        # Were we given a data object?
        if len(args) > 1:

            # Copy the query dict so we can mutate it.
            data = args[1]
            data = data.copy()

            # Get the management total forms count and add back in
            # the 1 we subtracted.
            total = data.get('mock_image-TOTAL_FORMS', 0)
            if total:
                total = int(total) + 1
            else:
                total = 1

            # Do a final check for the checkbox, if we are disabled
            # then set the count to 1.
            if not data.get('mock_image-apply_mock_image', False):
                total = 1

            data['mock_image-TOTAL_FORMS'] = total

            # Check for the existence of the other management form
            # elements and, if they're not there, add them in to
            # prevent errors.
            if 'mock_image-INITIAL_FORMS' not in data:
                data['mock_image-INITIAL_FORMS'] = 0
            if 'mock_image-MAX_NUM_FORMS' not in data:
                data['mock_image-MAX_NUM_FORMS'] = 1000

            # Also need to check for the apply mock image checkbox, due
            # to not using "from_xml" in certain places.
            self.apply_mock_image = data.get('mock_image-apply_mock_image', False)

        # Set to None if we aren't bound.
        else:
            data = None

        super(Form, self).__init__(data, *args[2:], **kwargs)

    def clean(self):

        # Get the checkbox state.
        self.apply_mock_image = self.data.get('mock_image-apply_mock_image', False)

    def to_xml(self, root):
        version = 2.0
        to_xml_2(self, root)

    @classmethod
    def from_xml(cls, ui_holder, xml_root, prefix=None):
        version = xml_root.xpath('//workflow/schema-version')
        if version and version[0].text == '2.0':
            return from_xml_2(cls, ui_holder, xml_root, prefix=prefix)
        else:
            return cls(ui_holder, {}, prefix=prefix)
