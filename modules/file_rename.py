# -*- coding: utf-8 -*-
import sys
import os
import io
import re

# Allowed types of files to be renamed.
ALLOWED_FILE_TYPES = ('.srt', '.sub', '.avi', '.mp4', '.mkv')

# Format to rename the file.
# WARNING: make sure to keep both placeholders (%s) or the script will fail.
FILE_RENAME_FORMAT = 'S%sE%s'


class FileRename():

	def rename_file(self, file_name):
		"""
		Process should happen in the following order:
		- check is this file allowed to be processed
		- check is the file containing 2 numbers
		- use the numbers to rename the file
		"""
		if not self.allowed_file_type(file_name):
			return '--> %s is not supported. No action taken.' % file_name

		# Get the general information about the file being renamed.
		file_location = os.path.dirname(file_name)
		original_file_name_with_ext = os.path.basename(file_name)
		original_file_name = os.path.splitext(original_file_name_with_ext)[0]
		original_file_ext = os.path.splitext(original_file_name_with_ext)[1]

		# Extract numbers from the original file name.
		# We expect at least two numbers.
		file_numbers_temp = re.findall(r'\d+', original_file_name)
		if len(file_numbers_temp) < 2:
			return '--> %s is supported but does not have 2 numbers in its name. No action taken.' % file_name
		# Kick all numbers with more then 2 digits, those are not tv show for sure.
		# We only run until we get two numbers, since thats what we require.
		file_numbers = []
		for fn in file_numbers_temp:
			# Once we reach 2 valid numbers we are done.
			if len(file_numbers) == 2:
				break
			if len(fn) > 2:
				continue
			if len(fn) == 1:
				fn = '0%s' % fn
			file_numbers.append(fn)

		# Generate new name for the file and full path with extension to it.
		new_file_name = FILE_RENAME_FORMAT % (file_numbers[0], file_numbers[1])
		new_file_full_name = os.path.join(file_location, new_file_name + original_file_ext)

		# Rename the file.
		os.rename(file_name, new_file_full_name)
		return '--> %s successfuly renamed to %s.' % (original_file_name, new_file_name)

	def process_directory(self, dir_path):
		"""
		Process should happen in the following order:
		- get the list of files available in the directory
		- if no files are found nothing will happen
		- if files are detected rename them one by one
		"""
		return_messages = []
		files = os.listdir(dir_path)
		if files:
			return_messages.append('Directory detected, attempting to process files:')
			for current_file in files:
				file_path = os.path.join(dir_path, current_file)
				# Try to rename if its a file, not another directory.
				if not os.path.isdir(file_path):
					return_messages.append(self.rename_file(file_path))
				else:
					return_messages.append('--> %s is a directory. No action taken.' % file_path)
		else:
			return_messages.append('Directory %s is empty. Aborting.' % dir_path)

		return return_messages

	def allowed_file_type(self, file_name):
		"""
		Check file has one of the allowed file extensions.
		Return boolean based on check.
		"""
		return file_name.lower().endswith(ALLOWED_FILE_TYPES)
