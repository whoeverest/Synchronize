import requests
import os
import inspect as i
import codecs

# TODO:
# - remove requests dependency

# Get the location of the file that imports 'synchronize'
# or use the current file location
if __name__ != "__main__":
    called_from = i.getframeinfo(i.getouterframes(i.currentframe())[1][0])[0]
else:
    called_from = os.path.abspath(__file__)


def get_files_for_sync():
    """ Walk the directory where the file is located and return a list of
    files that need to be synced.
    """
    current_dir = os.path.dirname(called_from)
    possible_files_for_sync = []
    for folder in os.walk(current_dir):
        for path in folder[2]:  # folder[2] is a list of files in the folder
            possible_files_for_sync.append(os.path.join(folder[0], path))
    files_for_sync = []
    for path in possible_files_for_sync:
        with open(path) as f:
            for line in f.readlines():
                if line.startswith("# url "):
                    files_for_sync.append(path)
                    break
    return files_for_sync


def read_source(url):
    """ Read the source from the given URL.
    """
    return requests.get(str(url)).text


def extract_url(text):
    """ Extract URL from comments, if any.
    """
    for line in text.splitlines():
        if line.startswith("# url "):
            return line.split()[2]
    return False


def update_file(file):
    """ Update the file with the remote source, if there are changes.
    """
    with codecs.open(str(file), 'r', 'utf-8') as f:
        local_source = f.read()
    url = extract_url(local_source)
    remote_source = read_source(url)
    print "Fetched " + url
    if local_source != remote_source:
        with codecs.open(str(file), 'w', 'utf-8') as f:
            f.write("# url %s\n" % url)
            f.write(remote_source)


# Slow and synchronous
for filename in get_files_for_sync():
    update_file(filename)


# Clean up the namespace
del(i)
del(os)
del(requests)
del(codecs)

del(get_files_for_sync)
del(read_source)
del(extract_url)
del(update_file)

del(called_from)
del(filename)

print dir()