import sublime, sublime_plugin, os
from . import pyyaml

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

            # Store every language (en, es, etc.) with the extension
            self.locales_path.add()

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
            yaml_dict = pyyaml.load(yaml_file)

            # Find the full paths file name key on the dict inside 
            root   = self.locales_path.locale_name()    # es
            dict_to_modify = yaml_dict[root]

            if self.selected_text.startswith("."):
                parent = self.locales_path.path.modelname() # model
                child  = self.locales_path.file_name()      # action

                # Move one level
                dict_to_modify = dict_to_modify[parent]

                # If the key doesn't exist create it
                if not child in dict_to_modify:
                    dict_to_modify[child] = {}

                # Move another level
                dict_to_modify = dict_to_modify[child]

                # Remove the dot    
                last_key = self.selected_text[1:]
            else:
                keys = self.selected_text.split(".")
                last_key = keys.pop()

                # Move on the yaml file
                for key in keys:
                    if not key in dict_to_modify:
                        dict_to_modify[key] = {}

                    dict_to_modify = dict_to_modify[key]

            # Add the selected text as a new key inside the file_name key with the text as a value
            dict_to_modify[last_key] = text

            # Save the file
            self.write_yaml_file(yaml_file, yaml_dict)

    def write_yaml_file(self, yaml_file, data_to_write):
        yaml_file.seek(0)
        yaml_file.write( pyyaml.dump(data_to_write, default_flow_style = False, allow_unicode=True, encoding = None) )
        yaml_file.truncate()

    def show_input_panel(self, message, on_done = None, on_change = None, on_cancel = None):
        self.view.window().show_input_panel(message, "", on_done, on_change, on_cancel)


class LocalesPath():
    def __init__(self, full_path):
        # Path helper
        self.path = Path(full_path)

        # Every locale will be stored here
        self.locales = Locales()

    def move_to_modelname(self):
        self.path.move_to_modelname()

    def add(self):
        self.locales.add(self.path.file_names(".yml"))

    def process(self):
        return self.locales.process()

    def yaml(self):
        return self.path.locales + self.locales.current_locale

    def modelname(self):
        return self.path.modelname()

    def file_name(self):
        return Path.remove_extension(self.path.file_name())

    def locale_name(self):
        return Path.remove_extension(self.locales.current_locale)


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
        self.locales = os.path.abspath(os.path.join(self.dirname(), "..", "..", "..", "config", "locales")) + "/"

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

    def file_extension(self, file_path = None):
        file_path = file_path or self.full
        return os.path.splitext(file_path)[1]

    def file_name(self, file_path = None):
        file_path = file_path or self.full
        return os.path.basename(file_path)

    @classmethod
    def remove_extension(cls, file_name):
        name, sep, ext = file_name.partition(".")
        return name
