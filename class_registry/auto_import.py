import os
from os import path


class AutoImport(object):

    def __init__(self, module):
        self.module = module

    def get_package_name(self, package_file_path):
        dotted_path = package_file_path.replace("/", ".")
        idx = dotted_path.index(self.module.__name__.replace("..", "."))
        return dotted_path[idx:]

    def get_module_name(self, f):
        return path.basename(f)[:-3]

    def filter_out_init_and_non_python_files(self, file_name):
        return file_name.endswith(".py") and not file_name.startswith("__")

    def setup(self):
        module_files = os.walk(path.abspath(path.dirname(self.module.__file__)))

        for file_path, _, files in module_files:
            for python_file_name in filter(self.filter_out_init_and_non_python_files, files):
                __import__(self.get_package_name(file_path) + "." + self.get_module_name(python_file_name))
