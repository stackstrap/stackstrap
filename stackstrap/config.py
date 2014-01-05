import errno
import logging
import os
import yaml

class Settings(object):
    def __init__(self, base_dir):
        self.log = logging.getLogger("settings")
        self.data = {}
        self.configure(base_dir)

    def configure(self, base_dir):
        self.base_dir = os.path.expanduser(base_dir)
        self.mkdir(self.base_dir)

        settings_file = os.path.join(base_dir, 'settings')
        settings_data = {}
        if os.path.exists(settings_file):
            self.log.debug("Attempting to load settings from: %s" % settings_file)
            try:
                data = open(settings_file).read()
            except OSError as e:
                self.log.error("Failed to load settings file (%s): %s" % (settings_file, e))
            else:
                try:
                    settings_data = yaml.safe_load(data)
                except yaml.error.YAMLError as e:
                    self.log.error("Failed to parse YAML data (%s): %s" % (settings_file, e))

        self.data = settings_data

        self.log.debug("%d settings loaded" % len(settings_data))

    def get(self, name, default=None):
        if name in self.data:
            return self.data[name]
        return default

    def set(self, name, val):
        self.data[name] = val

    def path(self, *parts):
        return os.path.join(self.base_dir, *parts)

    def mkdir(self, *parts):
        "Ensure a relative dir exists"
        dir_name = self.path(*parts)
        self.mkdir_p(dir_name)
        return dir_name

    def mkdir_p(self, dir_name):
        try:
            os.makedirs(dir_name, 0755)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
                pass
            else:
                raise

    def save(self):
        settings_file = os.path.join(self.base_dir, 'settings')
        with open(settings_file, 'w') as f:
            yaml.dump(self.data, f)

settings = Settings("~/.stackstrap")
