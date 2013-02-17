"""
==================
tao.ui_modules
==================

Helper class to extension UI modules
"""
from django.conf import settings
from tao.forms import OutputFormatForm, RecordFilterForm


class UIModulesHolder:
    def __init__(self, post=None):
        form_classes = [(__import__('taoui_%s.forms' % module_name).forms.Form, module_name)
                        for module_name in settings.MODULES] + \
                       [(RecordFilterForm,'record_filter'), (OutputFormatForm, 'output_format')]
        # forms are created _and_stored_ one by one so later forms can use data in first ones
        self._dict = {}
        self._forms = []
        for klass, module_name in form_classes:
            if post is None:
                form = klass(self, prefix=module_name)
            else:
                form = klass(self, post, prefix=module_name)
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
        vals = [v.is_valid() for v in self._forms]
        return all(vals)
