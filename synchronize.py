import urllib2
import os
import inspect as i
import codecs
import logging

# TODO:
# - Replace print statements with logging
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


def read_source(url):
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
        for line in f.readlines():
            if line.startswith("# url "):
                return line.split()[2]
    return False


def update_file(file):
    """ Update the file with the remote source.
    """
    url = extract_url(file)
    if not url:
        return False  # no url found in file
    remote_source = read_source(url)
    if not remote_source:
        return False  # URL fetch failed
    with codecs.open(str(file), 'w', 'utf-8') as f:
        f.write("# url %s\n" % url)
        f.write(remote_source)
    return True


# Get the location of the file that imports 'synchronize'.
# If the file wasn't imported, use the path of the current file.
if __name__ == "__main__":
    called_from = os.path.abspath(__file__)
else:
    called_from = i.getframeinfo(i.getouterframes(i.currentframe())[1][0])[0]

# Slow and synchronous
for filename in get_files(called_from):
    update_file(filename)


# Clean up the namespace...
# Imports:
del(i)
del(os)
del(urllib2)
del(codecs)
del(logging)

# Variables
del(called_from)
del(filename)

# Functions
del(get_files)
del(read_source)
del(extract_url)
del(update_file)

print dir()
