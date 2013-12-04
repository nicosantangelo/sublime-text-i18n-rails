import sublime, sublime_plugin
from I18nRails import pyyaml
from I18nRails.locales_path import LocalesPath

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
            self.show_input_panel(locale, self.process, None, self.process)

    def write_text(self, text):
        # Get the path of the yml file
        yaml_path = self.locales_path.yaml()

        # Transform it to an dic
        with open(yaml_path, 'r+') as yaml_file:
            yaml_dict = yaml_to_write = pyyaml.load(yaml_file)

            # Find the full paths file name key on the dict inside 
            keys = [ self.locales_path.locale_name() ] # root: es|en|...

            if self.selected_text.startswith("."):
                # [model, child]
                keys += [self.locales_path.path.modelname(), self.locales_path.file_name()]

                # Remove the dot    
                last_key = self.selected_text[1:]
            else:
                #[ key1, key2, ...]
                keys += self.selected_text.split(".")
                last_key = keys.pop()

            # Move on the yaml file
            yaml_dict = self.traverse_yml(yaml_dict, keys)

            # Add the selected text as a new key inside the file_name key with the text as a value
            yaml_dict[last_key] = text

            # Save the file
            self.write_yaml_file(yaml_file, yaml_to_write)

            self.display_message("{0}: {1} created!".format(last_key, text))

    def traverse_yml(self, yaml_dict, keys):
        for key in keys:
            if not key in yaml_dict or yaml_dict[key] is None:
                yaml_dict[key] = {}

            yaml_dict = yaml_dict[key]

        return yaml_dict

    def write_yaml_file(self, yaml_file, data_to_write):
        yaml_file.seek(0)
        yaml_file.write( pyyaml.dump(data_to_write, default_flow_style = False, allow_unicode = True, encoding = None) )
        yaml_file.truncate()

    def show_input_panel(self, message, on_done = None, on_change = None, on_cancel = None):
        self.view.window().show_input_panel(message, "", on_done, on_change, on_cancel)

    def display_message(self, text):
      sublime.active_window().active_view().set_status("i18_rails", text)