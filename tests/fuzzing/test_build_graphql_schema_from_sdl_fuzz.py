# import sys
#
# import afl
# from tartiflette.sdl.builder import build_graphql_schema_from_sdl
# from tartiflette.sdl.schema import GraphQLSchema

# We use American Fuzzy Loop for this.
# TODO: Do the same with libgraphqlparser (needs good security :) )
# Commented for the moment, so pytest won't complain.

# afl.init()
#
# try:
#     build_graphql_schema_from_sdl(sys.stdin.read(),
#                                   schema=GraphQLSchema())
# except ValueError:
#     pass
