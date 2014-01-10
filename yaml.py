import codecs
import pyyaml as pyyaml

class Yaml():
    def __init__(self, locales_path):
        self.locales_path = locales_path
        self.setup()

    def move_to(self, selected_text):
        # Find the full paths file name key on the dict inside 
        keys = [ self.locales_path.locale_name() ] # root: es|en|...

        if selected_text.startswith("."):
            # [model, child]
            keys += self.locales_path.splitted_keys()

            # Remove the dot    
            self.last_key = selected_text[1:]
        else:
            #[ key1, key2, ...]
            keys += selected_text.split(".")
            self.last_key = keys.pop()

        # Move on the yaml file
        self.traverse(keys)

        return self.dict

    def value_from(self, selected_text):
        self.read_file()

        self.move_to(selected_text)

        return self.dict[self.last_key] if self.last_key in self.dict else ""

    def write_text(self, text):
        with codecs.open(self.locales_path.yaml(), 'w', "utf-8") as yaml_file:
            self.dict[self.last_key] = text.encode('utf-8')

            self.write_file(yaml_file)

        return self

    def read_file(self):
        with codecs.open(self.locales_path.yaml(), 'r', "utf-8") as yaml_file:
            self.dict = self.yaml_to_write = pyyaml.load(yaml_file)

        return self.dict

    def write_file(self, yaml_file):
        yaml_file.seek(0)
        yaml_file.write( pyyaml.safe_dump(self.yaml_to_write, default_flow_style = False, allow_unicode = True, encoding = None) )
        yaml_file.truncate()

    def value_count(self, key):
        count = 0
        while self.locales_path.process():
            if self.value_from(key): 
                count += 1

        return count

    def traverse(self, keys):
        for key in keys:
            if not key in self.dict or self.dict[key] is None:
                self.dict[key] = {}

            self.dict = self.dict[key]

        return self.dict

    def setup(self):
        self.dict = {}
        self.yaml_to_write = {}
        self.last_key = ''
