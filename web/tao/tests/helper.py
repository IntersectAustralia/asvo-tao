import os, errno

def create_file(dir_path, filename, filenames_to_contents):    
    file_path = os.path.join(dir_path, filename)
    mkdir_p(os.path.dirname(file_path))
    with open(file_path, 'w') as f:
        f.write(filenames_to_contents[filename])
        
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