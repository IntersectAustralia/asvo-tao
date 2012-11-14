import os

def create_file(dir_path, filename, filenames_to_contents):
    file_path = os.path.join(dir_path, filename)
    with open(file_path, 'w') as f:
        f.write(filenames_to_contents[filename])