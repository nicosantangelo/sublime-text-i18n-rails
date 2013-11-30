import sublime, sublime_plugin, os
from . import pyyaml

class I18nRailsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# Path helper
		self.path = LocalesPath(self.view.file_name())

		# Every locale will be stored here
		self.locales = set()

		# Take highlighted text
		selections = self.view.sel()

		# For each selection
		for selection in selections:
			selected_text = self.view.substr(selection)

			# If the text starts with a dot, parse the text and search in ../config/locales/views/folder_name/*.yml
			if selected_text.startswith("."):
				self.path.move_to_modelname()

			# Store every language (en, es, etc.) with the extension
			self.locales |= set(self.path.file_names(".yml"))

			# Prompt an input to place the translation foreach language
			self.process_locales(None)


	def process_locales(self, user_text):
		# Write the files keeping in mind the presence (or lack of) a dot to place the keys in the yml
		if user_text:
			self.write_text(user_text)

		# Continue showing the prompts
		if len(self.locales) > 0:
			self.current_locale = self.locales.pop()
			self.show_input_panel(self.current_locale, self.process_locales)
		else:
			self.current_locale = None

	def write_text(self, text):
		yaml_path = self.path.locales_path + self.current_locale
		print(yaml_path)

		stream = open(yaml_path, 'r')
		print(pyyaml.load(stream))

	def show_input_panel(self, message, on_done):
		self.view.window().show_input_panel(message, "", on_done, None, None)

class LocalesPath():
	def __init__(self, full_path):
		self.full_path = full_path
		self.locales_path = os.path.abspath(os.path.join(self.dirname(), '..', '..', '..', 'config', 'locales'))

	def move_to_modelname(self):
		self.locales_path += "/views/" + self.modelname() + "/"
		return self

	def modelname(self):
		return os.path.split(self.dirname())[1]

	def dirname(self):
		return os.path.dirname(self.full_path)

	def file_names(self, extension = ""):
		return [f for f in os.listdir(self.locales_path) if self.is_file(f) and self.file_has_extension(f, extension)]

	def is_file(self, file_path):
		return os.path.isfile(os.path.join(self.locales_path, file_path))

	def file_has_extension(self, file_path, extension):
		return self.file_extension(file_path) == extension or extension == ""

	def file_extension(self, file_path):
		return os.path.splitext(file_path)[1]
