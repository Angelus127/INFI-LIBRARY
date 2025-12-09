import os, json, tempfile

def temp_create(media_cache):
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    with tempfile.NamedTemporaryFile(delete=False, mode='w', dir='tmp') as tmp_file:
        tmp_file.write(json.dumps(media_cache))
        temp_file_name = tmp_file.name
    return temp_file_name

def temp_read(temp_file_name):
    with open(temp_file_name, 'r') as tmp_file:
        media_cache = json.load(tmp_file)
    return media_cache

def temp_cleanup(temp_file_name):
    if os.path.exists(temp_file_name):
        os.remove(temp_file_name)