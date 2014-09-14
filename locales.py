class Locales():
    def __init__(self):
        self.names = set()
        self.current_locale = ""

    def add(self, file_names):
        self.names |= set(file_names)

    def process(self):
        self.current_locale = self.names.pop() if len(self.names) > 0 else None
        return self.current_locale

    def get(self, index):
        if index >= 0 and index < len(self.names):
            self.current_locale = list(self.names)[index]
            return self.current_locale
