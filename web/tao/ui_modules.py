"""
==================
tao.ui_modules
==================

Helper class to extension UI modules
"""
from django.conf import settings
from tao.record_filter_form import RecordFilterForm
from tao.output_format_form import OutputFormatForm
from tao.models import Simulation, GalaxyModel, DataSet

def _from_post(self, klass, module_name, param):
    if param is None:
        form = klass(self, prefix=module_name)
    else:
        form = klass(self, param, prefix=module_name)
    return form

def _from_xml(self, klass, module_name, param):
    if param is None:
        form = klass.from_xml(self, prefix=module_name)
    else:
        form = klass.from_xml(self, param, prefix=module_name)
    return form

class UIModulesHolder:

    form_classes = [(__import__('taoui_%s.forms' % module_name).forms.Form, module_name)
                    for module_name in settings.MODULES] + \
                   [(RecordFilterForm,'record_filter'), (OutputFormatForm, 'output_format')]

    # this 'constants' are methods that will become instance methods
    POST = _from_post
    XML = _from_xml

    def __init__(self, method, param=None):
        # forms are created _and_stored_ one by one so later forms can use data in first ones via self._dict = {}
        self._forms = []
        self._dict = {}
        self._errors = None
        self._dataset = None
        for klass, module_name in UIModulesHolder.form_classes:
            form = method(self, klass, module_name, param)
            self._forms.append(form)
            self._dict[module_name] = form


    def forms(self):
        return self._forms

    def is_bound(self, module_name):
        return self._dict[module_name].is_bound

    def raw_data(self, module_name, var_name):
        return self._dict[module_name].data[module_name + '-' + var_name]

    def cleaned_data(self, module_name, var_name):
        return self._dict[module_name].cleaned_data[var_name]

    def validate(self):
        valid = True
        if self._errors is None:
            self._errors = {}
        for v in self._forms:
            form_valid = v.is_valid()
            if not form_valid:
                if isinstance(v.errors, list):
                    # Assume a list of errors from a FormSet
                    for e in v.errors:
                        self._errors.update(e)
                else:
                    self._errors.update(v.errors)
            valid &= form_valid
        return valid

    @property
    def errors(self):
        if self._errors is None:
            self.validate()
        return self._errors

    @property
    def dataset(self):
        """Answer the dataset referenced by the receiver
        (through the selected Dark Matter Simulation and Galaxy Model)"""

        if self._dataset is None:
            sid = self.raw_data('light_cone', 'dark_matter_simulation')
            gmid = self.raw_data('light_cone', 'galaxy_model')
            self._dataset = DataSet.objects.get(simulation_id=sid, galaxy_model_id=gmid)
        return self._dataset
    