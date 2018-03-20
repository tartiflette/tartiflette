class Node():
    def __init__(self, path, gql_type, location, name):
        self.path = path
        self.parent = None
        self.graphql_type = gql_type
        self.location = location
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.graphql_type, self.name)
