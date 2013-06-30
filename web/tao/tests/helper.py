import os, errno

from tao.settings import MODULE_INDICES
from tao.xml_util import xml_parse

def create_file(dir_path, filename, filenames_to_contents):    
    file_path = os.path.join(dir_path, filename)
    mkdir_p(os.path.dirname(file_path))
    with open(file_path, 'w') as f:
        f.write(filenames_to_contents[filename])

def get_file_size(dir_path, file_name):
    file_path = os.path.join(dir_path, file_name)
    size = os.path.getsize(file_path)
    units = ['B', 'kB', 'MB']
    for x in units:
        if size < 1000:
            return '%3.1f%s' % (size, x)
        size /= 1000
    return '%3.1f%s' % (size, 'GB')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
        
def write_file_from_zip(zipfile_obj, filename, fullpath):
    with open(fullpath, 'wb') as outfile:
        outfile.write(zipfile_obj.read(filename))

def make_form(defaults, form_class, values, prefix=None, ui_holder=None):
    if prefix in defaults:
        default_values = defaults[prefix].copy()
    else:
        default_values = {}
    default_values.update(values)
    return form_class(ui_holder, dict([(prefix + '-'+ k,v) for k,v in default_values.iteritems()]), prefix=prefix)

def make_form_xml(form_class, xml_str, prefix=None, ui_holder=None):
    xml_root = xml_parse(xml_str)
    print xml_root
    return form_class.from_xml(ui_holder, xml_root, prefix=prefix)


class MockUIHolder:
    """
    Just a very simple mock of the UI Holder to make sure the RecordFilterForm works
    """
    def __init__(self, **kwargs):
        self._forms = kwargs

    def update(self, **kwargs):
        self._forms.update(kwargs)
        return self

    def is_bound(self, module_name):
        if module_name not in self._forms: raise Exception("I am mock!")
        return self._forms[module_name].is_bound

    def raw_data(self, module_name, var_name):
        if module_name not in self._forms: raise Exception(module_name + " not in self._forms")
        return self._forms[module_name].data[module_name + '-' + var_name]

    def cleaned_data(self, module_index, var_name):
        try:
            # module_index = int(float(MODULE_INDICES[module_name]))-1
            return self._forms[module_index].cleaned_data[var_name]
        except KeyError:
            print module_index + " not valid"

    def cleaned_data(self, module_name, var_name):
        if module_name not in self._forms: raise Exception(module_name + " not in self._forms")
        return self._forms[module_name].cleaned_data[var_name]

    def forms(self):
        return [v for k,v in self._forms.items()]

    def set_forms(self, forms):
        self._forms = forms
