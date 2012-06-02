# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import fileinput


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__).decode('utf-8')).replace('\\', '/')
EXTENSIONS = ('html', )
FILE_NAME_TO_WRITE = u'123.txt'


def get_files_by_extension():
	"""Scan files in CURRENT_PATH dir """
	files = []
	for filename in os.listdir(CURRENT_PATH):
		try:
			basename, extension = filename.split('.')
			if extension in EXTENSIONS:
				files.append(filename)
		except ValueError:
			pass
	if FILE_NAME_TO_WRITE in files:
		files.pop(files.index(FILE_NAME_TO_WRITE))

	EXCLUDE = ('__init__.py', 'tests.py', __file__)
	for file_name in EXCLUDE:
		try:
			files.pop(files.index(file_name))
		except ValueError:
			pass

	return files

print get_files_by_extension()
READED_FILES = get_files_by_extension()

with open(FILE_NAME_TO_WRITE, 'a+b') as header:
		header.write('\n\r' + u'Листинг HTML шаблонов приложения ' + \
			os.path.basename(os.getcwd()) + '\n\r')

for file_name in READED_FILES:
	with open(FILE_NAME_TO_WRITE, 'a+b') as header:
		header.write('\n\r' + u'Листинг шаблона ' + file_name + '\n\r')
	for line in fileinput.input(file_name):
		with open(FILE_NAME_TO_WRITE, 'a+b') as result:
			result.write(line)

