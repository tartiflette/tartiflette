"""
contains code for request execution hooks base
classes and managements

pre-parse(ctx, req)
post-parse(ctx, r_node)
pre-exec(ctx, r_node)
if any errors on-error(g_ctx, errors_list)
post-exec(ctx, results)
pre-serialize(ctx, results)
post-serialize(ctx, serialized)
"""
