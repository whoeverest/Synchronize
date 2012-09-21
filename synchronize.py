import urllib2
import os
import inspect as i
import codecs
import logging


# Get the location of the file that imports 'synchronize'.
# If the file wasn't imported, use the path of the current
# file.
if __name__ == "__main__":
    called_from = os.path.abspath(__file__)
else:
    called_from = i.getframeinfo(i.getouterframes(i.currentframe())[1][0])[0]


def get_files_for_sync():
    """ Walks the directory where the file is located and returns a list of
    files that need to be synchronized.
    """
    current_dir = os.path.dirname(called_from)
    dir_paths = []
    for folder in os.walk(current_dir):
        for path in folder[2]:  # folder[2] is a list of files in the folder
            dir_paths.append(os.path.join(folder[0], path))
    files_for_sync = []
    for path in dir_paths:
        with open(path) as f:
            for line in f.readlines():
                if not line.startswith("# url "):
                    break
                files_for_sync.append(path)
    return files_for_sync


def read_source(url):
    """ Read the source from the given URL.
    """
    try:
        return urllib2.urlopen(str(url)).read()
    except urllib2.URLError, e:
        print "There was a error when fetching '%s':" % url
        print e
        print "Corresponding file won't be synchronized."


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
    if not remote_source:
        print "Could not load " + url
        return
    else:
        print "Fetched " + url
    if local_source != remote_source:
        with codecs.open(str(file), 'w', 'utf-8') as f:
            f.write("# url %s\n" % url)
            f.write(remote_source)


# Slow and synchronous
for filename in get_files_for_sync():
    update_file(filename)


# Clean up the namespace:
#
# Imports:
del(i)
del(os)
del(urllib2)
del(codecs)
del(logging)

# Variables
del(called_from)

# Functions
del(get_files_for_sync)
del(read_source)
del(extract_url)
del(update_file)
