import sublime, sublime_plugin, re
from .locales_path import LocalesPath
from .yaml import Yaml

class I18nRailsToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global i18n_rails_keys_enabled

        # Common operations
        self.helper = CommandHelper(self)

        if not self.helper.in_view():
            self.display_message("This package only works on rails views!")
            return 

        self.regions = { 'valid': ([], "comment"), 'partial': ([], "string"), 'invalid': ([], "invalid") }

        # Default value
        if not 'i18n_rails_keys_enabled' in globals():
            i18n_rails_keys_enabled = True 

        if i18n_rails_keys_enabled:
            self.highlight_keys()
        else:
           self.clear_highlighted_keys()

        i18n_rails_keys_enabled = not i18n_rails_keys_enabled

    def highlight_keys(self):
        self.locales_path = LocalesPath(self.view.file_name())
        self.yaml = Yaml(self.locales_path)

        method_call_regions = self.view.find_all('\s*(?:I18n\.)?t(?:\(|\s+)["\'](\.?[\w\.]+)["\']\)?\s*')

        for method_call_region in method_call_regions:
            key = self.find_key_in_method_call(method_call_region)
            
            if self.helper.find_files_according_to(key):
                self.add_to_regions(method_call_region, key)

        self.paint_highlighted_keys()

    def find_key_in_method_call(self, method_call_region):
        return re.search('["\'](\.?[\w\.]+)["\']', self.view.substr(method_call_region)).group(1)

    def add_to_regions(self, region, key):
        locales_len = self.locales_path.locales_len()
        translations_count = self.yaml.text_count(key)

        if translations_count == locales_len:
            self.regions['valid'][0].append(region)
        elif translations_count > 0:
            self.regions['partial'][0].append(region)
        else:
            self.regions['invalid'][0].append(region)

    def paint_highlighted_keys(self):
        for region_name, regions_tuple in self.regions.items():
            self.view.add_regions(region_name, regions_tuple[0], regions_tuple[1], "", sublime.DRAW_NO_FILL)

    def clear_highlighted_keys(self):
        for region_name in self.regions.keys():
            self.view.erase_regions(region_name)

    def display_message(self, text):
        sublime.active_window().active_view().set_status("i18_rails", text)

class I18nRailsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Common operations
        self.helper = CommandHelper(self)

        if not self.helper.in_view():
            self.display_message("This package only works on rails views!")
            return 

        # Facade between path and locales
        self.locales_path = LocalesPath(self.view.file_name())

        # Object to read and parse a yaml file
        self.yaml = Yaml(self.locales_path)

        # Take highlighted text
        selection_regions = self.view.sel()

        # Check if there's a selection
        if not selection_regions[0].empty():
            self.process_regions(selection_regions)
        else:
            self.view.run_command("expand_selection", { "to": "scope" }) 
            selection_regions = self.view.sel()
            self.process_regions(selection_regions)

    def process_regions(self, selection_regions):
        # For each selection
        for region in selection_regions:
            self.selected_text = self.view.substr(region)

            if re.match('^["\'].+["\']$', self.selected_text):
                self.selected_text = self.selected_text[1:-1]

            if self.helper.find_files_according_to(self.selected_text):
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
        return self.yaml.text_from(self.selected_text)

    def write_text(self, text):
        self.yaml.write_text(text)
        self.display_message("{0}: {1} created!".format(self.selected_text, text))

    def show_input_panel(self, caption, initial_text = "", on_done = None, on_change = None, on_cancel = None):
        self.view.window().show_input_panel(caption, initial_text, on_done, on_change, on_cancel)

    def display_message(self, text):
        sublime.active_window().active_view().set_status("i18_rails", text)

class CommandHelper():
    def __init__(self, command):
        self.command = command
        # Get the rejected file names from the settings
        settings = sublime.load_settings("I18nRails.sublime-settings")
        self.rejected_files = settings.get("rejected_files", [])

    def in_view(self):
        return bool(re.search(r'\.(erb|haml)?$', self.command.view.file_name()))

    def find_files_according_to(self, key):
        # If the text starts with a dot, parse the text and search in ../config/locales/views/folder_name/*.yml, else in ../config/locales/
        self.command.locales_path.reset()

        if key.startswith("."):
            self.command.locales_path.move_to_translation_folder()

        try:
            # Store every language (en, es, etc.) with the extension, except for the rejected files
            self.command.locales_path.add(self.rejected_files)
            return True
        except FileNotFoundError:
            self.command.display_message(self.command.locales_path.yaml() + " doesn't exist. Are you in a view?")
        