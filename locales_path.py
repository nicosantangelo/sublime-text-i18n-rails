from .locales import Locales
from .path    import Path

class LocalesPath():
    def __init__(self, full_path):
        # Path helper
        self.path = Path(full_path)

        # Every locale will be stored here
        self.locales = Locales()

    def move_to_modelname(self):
        self.path.move_to_modelname()

    def go_back(self):
        self.path.go_back()

    def add(self):
       self.locales.add(self.path.file_names(".yml"))

    def process(self):
        return self.locales.process()

    def yaml(self):
        return self.path.locales + self.locales.current_locale

    def modelname(self):
        return self.path.modelname()

    def file_name(self):
        file_name = Path.remove_extension(self.path.file_name())
        return file_name[1:] if file_name.startswith("_") else file_name

    def locale_name(self):
        return Path.remove_extension(self.locales.current_locale)

    def locales_len(self):
        return len(self.locales.names)