from .locales import Locales
from .path    import Path

class LocalesPath():
    def __init__(self, full_path):
        # Path helper
        self.path = Path(full_path)

        # Every locale will be stored here
        self.locales = Locales()

    def move_to_translation_folder(self):
        self.path.move_to_translation_folder()

    def reset(self):
        self.path.reset()

    def add(self, rejected = []):
        self.locales.add(self.path.file_names(".yml", rejected))

    def for_each_process(self, func):
        locale = self.process()
        while locale:
            func(locale)
            locale = self.process()

    def process(self):
        return self.locales.process()

    def yaml(self):
        return self.path.i18n + self.locales.current_locale

    def locale_name(self):
        return Path.remove_extension(self.locales.current_locale)

    def locales_len(self):
        return len(self.locales.names)

    def splitted_keys(self):
        return self.path_after_views().split("/") + [self.rails_view_file_name()]

    def path_after_views(self):
        return self.path.after_views()

    def rails_view_file_name(self):
        file_name = Path.remove_extension(self.path.file_name())
        return file_name[1:] if file_name.startswith("_") else file_name