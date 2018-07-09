class Node:
    def __init__(self, path, libgraphql_type, location, name):
        self.path = path
        self.parent = None
        self.libgraphql_type = libgraphql_type
        self.location = location
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.libgraphql_type, self.name)
