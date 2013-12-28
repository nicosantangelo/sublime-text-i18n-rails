import os

class Path():
    def __init__(self, full_path):
        self.full = full_path
        self.i18n = self.default_path()

    def default_path(self):
        app_index = self.dirname().index("/app")
        return os.path.abspath(os.path.join(self.dirname()[:app_index], "config", "locales")) + "/"

    def move_to_translation_folder(self, new_path = None):
        """Recursive method: Searches for the directory containing the translations and moves up if it doesn't find it.
        It will stop searching if the base path was reached. It requires self.i18n to be reseted to be used."""
        new_path = new_path or self.i18n + "views/" + self.after_views() + "/"

        if os.path.isdir(new_path):
            self.i18n = new_path 
        else:
            new_path = os.path.abspath(os.path.join(new_path, os.pardir))
            if os.path.split(new_path)[1] == 'views':
                self.i18n = self.default_path()
            else:
                self.move_to_translation_folder(new_path + "/")

        return self

    def reset(self):
        self.i18n = self.default_path()
        return self

    def after_views(self):
        return self.dirname().split("/views/")[1]

    def dirname(self):
        return os.path.dirname(self.full)

    def file_names(self, extension = "", rejected = []):
        return [f for f in os.listdir(self.i18n) if self.is_file(f) and self.file_has_extension(f, extension) and f not in rejected]

    def is_file(self, file_path):
        return os.path.isfile(os.path.join(self.i18n, file_path))

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