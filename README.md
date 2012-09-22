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
When `import synchronize` gets executed, it searches through files located in the 
caller's location. If they contain a `# url`, the script updates their content
with the data downloaded from the provided url.

# Example
main_file.py:

	```python
	import synchronize  # should be the first thing that gets executed
	import matz

	print matz.add(2, 3)
	print matz.subtract(5, 2)
	```

matz.py

	```python
	# url https://raw.github.com/gist/3756905/
	def add(a, b):
		return a + b

	def subtract(a, b):
		return a - b
	```

Now every time I run `main_file.py`, Synchronize updates the contents of
`matz.py` with the contents of the Gist.