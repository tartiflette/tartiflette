class Node:
    def __init__(self, path, libgraphql_type, location, name):
        self.path = path
        self.parent = None
        self.children = []
        self.libgraphql_type = libgraphql_type
        self.location = location
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.libgraphql_type, self.name)

    def add_child(self, node):
        self.children.append(node)

    def set_parent(self, node):
        self.parent = node
