import logging

from aiohttp import web
import rapidjson as json

logger = logging.getLogger(__name__)


def _format_errors(errors):
    def format_error(_):
        formatted_error = {
            "type": "internal_error",
            "message": "Server internal",
        }
        return formatted_error

    results = []
    for error in errors:
        formatted_errors = format_error(error)
        if not isinstance(formatted_errors, list):
            formatted_errors = [formatted_errors]
        results += formatted_errors
    return results


class BadRequestError(Exception):
    pass


def prepare_response(data):
    headers = {}
    #  Do things with header here if needed

    return web.json_response(data, headers=headers, dumps=json.dumps)


# pylint: disable=too-many-locals
# reason: we're building a query with many components
async def _handle_query(req, query, query_vars, query_name):

    formatted_errors = None

    try:
        context = {"userdata": {}}

        query_result = await req.app["gql_engine"].execute(
            query=query, variables=query_vars, context=context
        )

    except Exception as e:  # pylint: disable=broad-except
        logger.exception(e)
        formatted_errors = _format_errors([e])

    if formatted_errors:  # There was an exception
        data = {"data": None, "errors": formatted_errors}
    else:
        data = query_result

    resp = prepare_response(data)

    resp.log = {
        "errors": data["errors"] if "errors" in data else None,
        "query_name": query_name,
        "query": query,
        "query_vars": None if query_vars is None else query_vars,
    }

    return resp


async def _post_params(req):
    try:
        req_content = await req.json(loads=json.loads)
    except Exception:  # pylint: disable=broad-except
        raise BadRequestError("Body should be a JSON object")

    if "query" not in req_content:
        raise BadRequestError('The mandatory "query" parameter is missing.')

    variables = None
    if "variables" in req_content and req_content["variables"] != "":
        variables = req_content["variables"]
        try:
            if isinstance(variables, str):
                variables = json.loads(variables)
        except Exception:  # pylint: disable=broad-except
            raise BadRequestError(
                'The "variables" parameter is invalid. '
                "A JSON mapping is expected."
            )

    return (req_content["query"], variables, req_content.get("operationName"))


async def handle_post(req):
    try:
        qry, qry_vars, qry_name = await _post_params(req)
        return await _handle_query(req, qry, qry_vars, qry_name)
    except BadRequestError as e:
        data = {"data": None, "errors": _format_errors([e])}
        return prepare_response(data)
