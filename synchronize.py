import os
import urllib2
import inspect as i
import codecs
import multiprocessing

# TODO:
# - Replace print statements with logging
# - Handle hashbangs
# - Refractor silent mode


# Maximum number of processes the script can spawn;
# If less then MAX_PR files are found for synchronization,
# len(files_for_sync) processes are spawned
settings = {
    'MAX_PR': 5,
    'SILENT': True,
}


def get_files(called_from):
    """ Returns a list of all the filenames in the callers directory.
    """
    current_dir = os.path.dirname(called_from)
    files = []
    for folder in os.walk(current_dir):
        for path in folder[2]:  # folder[2] is a list of files in the folder
            files.append(os.path.join(folder[0], path))
    return files


def read_remote(url):
    """ Read the source from the given URL.
    """
    try:
        return urllib2.urlopen(str(url)).read()
    except urllib2.URLError, e:
        if not settings['SILENT']:
            print
            print "There was a error when fetching '%s':" % url
            print e
            print "Corresponding file won't be synchronized.\n"


def extract_url(file):
    """ Extract URL from comments, if any.
    """
    with open(file) as f:
        line = f.readline()
        if line.startswith("# url "):
            return line.split()[2]


def update_file(file):
    """ Update the file with the remote source.
    """
    url = extract_url(file)
    if url is None:
        return
    remote_source = read_remote(url)
    if remote_source is None:
        return
    with codecs.open(str(file), 'w', 'utf-8') as f:
        f.write("# url %s\n" % url)
        f.write(remote_source)
    if not settings['SILENT']:
        print "Updated %s" % os.path.basename(file)
    return True


# Get the location of the file that imports 'synchronize'.
# If the file wasn't imported, use the path of the current file.
if __name__ == "__main__":
    called_from = os.path.abspath(__file__)
else:
    called_from = i.getframeinfo(i.getouterframes(i.currentframe())[1][0])[0]

# Update the files
files_for_sync = get_files(called_from)
max_processes = max(settings['MAX_PR'], len(files_for_sync))
if files_for_sync:
    pool = multiprocessing.Pool(processes=max_processes)
    pool.map(update_file, files_for_sync)

# Clean up the namespace...
# Imports:
del(i)
del(os)
del(urllib2)
del(codecs)
del(multiprocessing)

# Variables
del(settings)
del(called_from)
del(files_for_sync)
del(max_processes)

# Functions
del(get_files)
del(read_remote)
del(extract_url)
del(update_file)
del(pool)
