import sublime, sublime_plugin, os
from . import pyyaml

class I18nRailsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# Path helper
		self.path = Path(self.view.file_name())

		# Every locale will be stored here
		self.locales = Locales()

		# Take highlighted text
		selections = self.view.sel()

		# For each selection
		for selection in selections:
			selected_text = self.view.substr(selection)

			# If the text starts with a dot, parse the text and search in ../config/locales/views/folder_name/*.yml
			if selected_text.startswith("."):
				self.path.move_to_modelname()

			# Store every language (en, es, etc.) with the extension
			self.locales.add(self.path.file_names(".yml"))

			# Prompt an input to place the translation foreach language
			self.process_locales(None)

	def process_locales(self, user_text):
		# Write the files keeping in mind the presence (or lack of) a dot to place the keys in the yml
		if user_text:
			self.write_text(user_text)

		if self.locales.process():
			self.show_input_panel(self.locales.current_locale, self.process_locales)

	def write_text(self, text):
		# Get the path of the yml file
		yaml_path = self.path.locales + self.locales.current_locale
		print(yaml_path)

		# Transform it to an dic
		stream = open(yaml_path, 'r')
		print(pyyaml.load(stream))

		# Final result (dot)
		#  locale_name: 
		#    modelname:
		#      file_name:
		#        selected_text: text

		# Find the full path file name key on the dict inside 

		# If it doesn't exist create it

		# Add the selected text (removing the dot) as a new key inside the file_name key with the text as a value

		# Save the file

	def show_input_panel(self, message, on_done):
		self.view.window().show_input_panel(message, "", on_done, None, None)


class Locales():
	def __init__(self):
		self.locales = set()
		self.current_locale = ""

	def add(self, file_names):
		self.locales |= set(file_names)

	def process(self):
		self.current_locale = self.locales.pop() if len(self.locales) > 0 else None
		
		return self.current_locale


class Path():
	def __init__(self, full_path):
		self.full = full_path
		self.locales = os.path.abspath(os.path.join(self.dirname(), '..', '..', '..', 'config', 'locales'))

	def move_to_modelname(self):
		self.locales += "/views/" + self.modelname() + "/"
		return self

	def modelname(self):
		return os.path.split(self.dirname())[1]

	def dirname(self):
		return os.path.dirname(self.full)

	def file_names(self, extension = ""):
		return [f for f in os.listdir(self.locales) if self.is_file(f) and self.file_has_extension(f, extension)]

	def is_file(self, file_path):
		return os.path.isfile(os.path.join(self.locales, file_path))

	def file_has_extension(self, file_path, extension):
		return self.file_extension(file_path) == extension or extension == ""

	def file_extension(self, file_path):
		return os.path.splitext(file_path)[1]
