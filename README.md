# What is Synchronize?
Synchronize is a tiny Python script that let's you synchronize local files with
files you have on the Internet.

# How do I use it?
Add `import synchronize` as the first statement in your Python file. This means
you want to synchronize files located in the same place as your script, or
somewhere in the subdirectories. 

Then, add a `# url http://yourremoteurl.com/file_for_sync.py` comment in every 
file you want synced.

And that's it.

# How it works
When `import synchronize` gets executed it searches the caller's location and 
subfolders for files containing `# url` comment. If they contain it, their source 
is replaced with the remote version.