
def visualize_gql_tree_and_data(gql_nodes, current_level, value='result'):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    print("\n\n================ TTFTT Tree (%s) ===============================" % value)
    for level, nodes in enumerate(gql_nodes):
        star = "*" if level == current_level else " "
        print("Level#{}{}: ".format(level, star), end="")
        for node in nodes:
            node_color = FAIL if node.error else OKBLUE
            print("{}  {}<{}>  {}".format(node_color, node.name, getattr(node, value), ENDC), end="")
        print("")
