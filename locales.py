class Locales():
    def __init__(self):
        self.locales = set()
        self.current_locale = ""

    def add(self, file_names):
        self.locales |= set(file_names)

    def process(self):
        self.current_locale = self.locales.pop() if len(self.locales) > 0 else None
        return self.current_locale