import urllib2
import os
import inspect as i
import codecs
from multiprocessing import Process

# TODO:
# - Replace print statements with logging
# - Handle hashbangs
# - Hack to implement threads?


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
        print "There was a error when fetching '%s':" % url
        print e
        print "Corresponding file won't be synchronized."


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
        return False  # no url found in file
    remote_source = read_remote(url)
    if remote_source is None:
        return False  # URL fetch failed
    with codecs.open(str(file), 'w', 'utf-8') as f:
        f.write("# url %s\n" % url)
        f.write(remote_source)
    print "Updated %s" % os.path.basename(file)
    return True


# Get the location of the file that imports 'synchronize'.
# If the file wasn't imported, use the path of the current file.
if __name__ == "__main__":
    called_from = os.path.abspath(__file__)
else:
    called_from = i.getframeinfo(i.getouterframes(i.currentframe())[1][0])[0]

processes = []
for filename in get_files(called_from):
    p = Process(target=update_file, args=(filename,))
    p.start()
    processes.append(p)
for p in processes:
    p.join()


# Clean up the namespace...
# Imports:
del(i)
del(os)
del(urllib2)
del(codecs)
del(Process)

# Variables
del(called_from)
del(filename)

# Functions
del(get_files)
del(read_remote)
del(extract_url)
del(update_file)
del(processes)
del(p)

print dir()