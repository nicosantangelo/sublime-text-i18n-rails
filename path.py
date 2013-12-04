import os

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