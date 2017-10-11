# -*- coding: utf-8 -*-
import sys
import os
import io

# Characters to be replaced in the file content.
CHARS_TO_REPLACE = {
	'È': 'Č',
	'Æ': 'Ć',
	'è': 'č',
	'æ': 'ć',
	'ð': 'đ'
}
# Allowed types of files to be processed.
ALLOWED_FILE_TYPES = ('.srt', '.txt', '.sub')

# Define encoding values.
# There is no way to apsulutely correctly quess origin encoding so doing an educated guess.
# Change settings if working with different origin encoding.
SOURCE_ENCODING = 'cp1250'
DESTINATION_ENCODING = 'utf8'


class CharReplace():

	def process_file(self, file_name):
		"""
		Process should happen in the following order:
		- check is this file allowed to be processed
		- open the file in read mode and get its content
		- transfer the content to destination encoding format
		- close the file and open it again for writing in destination encoding
		- process the content by replacing all specified characters
		- write the new content to the file and close it
		"""
		if not self.allowed_file_type(file_name):
			return '--> %s is not supported. No action taken.' % file_name

		read_file = io.open(file_name, 'r', encoding=SOURCE_ENCODING)
		# Only start the process if the file is not already processed or already has characters.
		read_file_content = read_file.read()
		char_found, char_found_message = self.is_file_already_processed(read_file_content, file_name)
		if char_found:
			return char_found_message
		else:
			read_file_content = read_file_content.encode(DESTINATION_ENCODING)
			read_file.close()

			write_file = io.open(file_name, 'w', encoding=DESTINATION_ENCODING)
			write_file_content = self.replace_characters(read_file_content)
			write_file.write(write_file_content)
			write_file.close()
			return '--> %s successfuly processed.' % file_name

	def is_file_already_processed(self, file_content, file_name):
		"""
		Check do we have characters we want to replace already in the file.
		In case they exist we skip this file.
		"""
		char_found = False
		message = ''
		file_content_to_search = file_content.encode(SOURCE_ENCODING)
		for des_char, char in CHARS_TO_REPLACE:
			if char in file_content_to_search:
				char_found = True
				break
		if char_found:
			message = '--> %s already processed, skipping...' % file_name
		return char_found, message

	def process_directory(self, dir_name):
		"""
		Process should happen in the following order:
		- get the list of files available in the directory
		- in no files are found nothing will happen
		- in some files are detected print the message we found a directory and process them one by one
		"""
		return_messages = []
		files = os.listdir(dir_name)
		if files:
			return_messages.append('Directory detected, attempting to process files:')
			for current_file in files:
				file_path = os.path.join(dir_name, current_file)
				return_messages.append(self.process_file(file_path))
		else:
			return_messages.append('Directory %s is empty. Aborting.' % dir_name)

		return return_messages

	def process_based_on_type(self, file_path):
		"""
		Call the appropriate method based on is the path file or a directory.
		"""
		# Is this a file?
		if os.path.isfile(file_path):
			self.process_file(file_path)
		# Or is it a directory?
		elif os.path.isdir(file_path):
			self.process_directory(file_path)

	def replace_characters(self, content_to_change):
		"""
		Replace the characters in the content sent using CHARS_TO_REPLACE values.
		"""
		for old_char, new_char in CHARS_TO_REPLACE.iteritems():
			content_to_change = content_to_change.replace(old_char, new_char)

		return unicode(content_to_change, DESTINATION_ENCODING)

	def allowed_file_type(self, file_name):
		"""
		Check is file has one of the allowed file extensions.
		Return boolean based on check.
		"""
		return file_name.lower().endswith(ALLOWED_FILE_TYPES)
