from tartiflette.sdl import parse_graphql_sdl_to_ast, transform_ast_to_schema


def main():
    print(
        "Welcome to the Tartiflette GraphQL Schema Definition Language (SDL)"
    )
    print("helper CLI. This tool allows for easy testing of your GraphQL SDL.")
    print()
    while True:
        try:
            print("Please enter your schema WITHOUT BLANK LINES.")
            print("A blank line will trigger the parsing and printing of your")
            print("awesome schema. Press Ctrl+C to quit.")
            print("And remember, stay cool.")
            lines = []
            while True:
                line = input('> ')
                if line:
                    lines.append(line)
                else:
                    print("Blank line detected. Parsing...")
                    break
            full_sdl = ''.join(lines)
            raw_tree = parse_graphql_sdl_to_ast(full_sdl)
            print("Raw parser tree from SDL:")
            print(raw_tree.pretty())
            print("Transforming raw tree into GraphQLSchema...")
            print(transform_ast_to_schema(full_sdl, raw_tree))
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == '__main__':
    main()
