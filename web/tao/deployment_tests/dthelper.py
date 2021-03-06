import os
import errno
import codecs

from settings import MODULE_INDICES
from tao.xml_util import xml_parse

def get_file_size(dir_path, file_name):
    file_path = os.path.join(dir_path, file_name)
    size = os.path.getsize(file_path)
    units = ['B', 'kB', 'MB']
    for x in units:
        if size < 1000:
            return '%3d%s' % (round(size), x)
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

class MockUIHolder:
    """
    Just a very simple mock of the UI Holder to make sure the RecordFilterForm works
    """
    def __init__(self, **kwargs):
        self._forms = kwargs
        self._dataset = None

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

    def get_dataset(self):
        """Answer the dataset referenced by the receiver
        (through the selected Dark Matter Simulation and Galaxy Model)"""

        if self._dataset is None:
            raise Exception("I am poorly configured mock without _dataset")
        return self._dataset

    def set_dataset(self, v):
        self._dataset = v

    dataset = property(get_dataset, set_dataset)
