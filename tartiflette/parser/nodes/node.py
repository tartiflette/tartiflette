
class Node:
    def __init__(self, path, libcffi_type, location, name):
        self.path = path
        self.parent = None
        self.libcffi_type = libcffi_type
        self.location = location
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.libcffi_type, self.name)
