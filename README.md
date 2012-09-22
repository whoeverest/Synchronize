# What is Synchronize?
Synchronize is a tiny Python script that let's you synchronize local files with
files you have on the Internet.

Add `import synchronize` as first line in the main file and 
`# url https://yoururl.com/file-for-sync.py` in every file you want synchronized.
That's it, that simple.

# How it works
There are two things you need to add for the script to work: 

- the `import synchronize` statement and 
- the '# url http://yoururl.com' comment

When `import synchronize` gets executed (you should put that in the main file)
it searches the caller's location and subfolders for files containing `# url`
comment. If they contain it, their source is replaced with the remote version.