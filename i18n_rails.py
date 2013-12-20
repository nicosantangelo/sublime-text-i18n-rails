import sublime, sublime_plugin
from .locales_path import LocalesPath
from .yaml import Yaml

class I18nRailsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Facade between path and locales
        self.locales_path = LocalesPath(self.view.file_name())

        # Take highlighted text
        selections = self.view.sel()

        # For each selection
        for selection in selections:
            self.selected_text = self.view.substr(selection)

            # If the text starts with a dot, parse the text and search in ../config/locales/views/folder_name/*.yml
            if self.selected_text.startswith("."):
                self.locales_path.move_to_modelname()

            try:
                # Store every language (en, es, etc.) with the extension
                self.locales_path.add()
            except FileNotFoundError:
                self.display_message(self.locales_path.yaml() + " doesn't exist. Are you in a view?")
                continue

            # Prompt an input to place the translation foreach language
            self.process()

    def process(self, user_text = None):
        # Write the files keeping in mind the presence (or lack of) a dot to place the keys in the yml
        if user_text:
            self.write_text(user_text)

        locale = self.locales_path.process()
        if locale:
            existing_text = self.existing_text_from_yaml()
            self.show_input_panel(locale, existing_text, self.process, None, self.process)

    def existing_text_from_yaml(self):
        self.yaml = Yaml(self.locales_path)
        return self.yaml.text_from(self.selected_text)

    def write_text(self, text):
        self.yaml.write_text(text)

        self.display_message("{0}: {1} created!".format(self.selected_text, text))

    def show_input_panel(self, caption, initial_text = "", on_done = None, on_change = None, on_cancel = None):
        self.view.window().show_input_panel(caption, initial_text, on_done, on_change, on_cancel)

    def display_message(self, text):
      sublime.active_window().active_view().set_status("i18_rails", text)