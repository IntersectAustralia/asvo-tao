import os, errno

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
        default_values = defaults[prefix]
    else:
        default_values = {}
    default_values.update(values)
    return form_class(ui_holder, dict([(prefix + '-'+ k,v) for k,v in default_values.iteritems()]), prefix=prefix)

class MockUIHolder:
    """
    Just a very simple mock of the UI Holder to make sure the RecordFilterForm works
    """
    def __init__(self, light_cone_form):
        self.light_cone_form = light_cone_form

    def is_bound(self, module_name):
        if module_name != 'light_cone': raise Exception("I am mock!")
        return self.light_cone_form.is_bound

    def raw_data(self, module_name, var_name):
        if module_name != 'light_cone': raise Exception("I am mock!")
        return self.light_cone_form.data[module_name + '-' + var_name]

    def cleaned_data(self, module_name, var_name):
        if module_name != 'light_cone': raise Exception("I am mock!")
        return self.light_cone_form.cleaned_data[var_name]

    def forms(self):
        return self._forms

    def set_forms(self, forms):
        self._forms = forms
