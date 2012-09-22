# What is Synchronize?
Synchronize is a tiny Python script that let's you synchronize local files with
files you have on the Internet just by typing `import synchronize` at the
beginning of your script. It's not Git, it just downloads the source every
time you run your program, making sure you are running the newest copy.

# Example
Let's say you're working on a `matz` module:

	# matz.py
	def add(a,b):
		return a + b

	def subtract(a,b):
		return a - b

and you are using your module in a script:
	
	# main-program.py
	import matz

	print matz.add(2,3)
	print matz.subtract(5,3)

Right. But the thing is, you are collaborating and editing 'matz.py', so every
time you change something, you copy + paste the new version. Well, why not just
add a `# url https://remotesources.com/matz.py` and let the script handle the
rest?

# How it works
There are two things you need to add for the script to work: 

- the `import synchronize` statement and 
- the '# url http://yoururl.com' comment

When `import synchronize` gets executed (you should put that in the main file)
it searches the caller's location and subfolders for files containing `# url`
comment. If they contain it, their source is replaced with the remote version.

And that's it.