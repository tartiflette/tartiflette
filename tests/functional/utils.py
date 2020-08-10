from unittest.mock import MagicMock


class AsyncMock(MagicMock):
    """ Fix to be able to use MagicMock with async context"""

    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


def is_expected(result, expected):
    assert set(result.keys()) == set(expected.keys())
    assert len(result.keys()) == len(result.keys())
    assert result.get("data") == expected.get("data")
    if "errors" in expected:
        assert len(result["errors"]) == len(expected["errors"])
        not_found = []
        for expected_error in expected["errors"]:
            is_found = False
            for result_error in result["errors"]:
                if expected_error == result_error:
                    is_found = True
            if not is_found:
                not_found.append(expected_error)
        if not_found:
            raise AssertionError(
                "Following expected errors wasn't found: {}".format(
                    ", ".join(
                        [str(expected_error) for expected_error in not_found]
                    )
                )
            )


def assert_unordered_lists(list_a, list_b):
    assert len(list_a) == len(list_b)

    is_valid = True
    for item_a in list_a:
        if item_a not in list_b:
            is_valid = False
            break

    if not is_valid:
        raise AssertionError(
            f"Both list don't contains the same items: < {list_a} > "
            f"- < {list_b} >."
        )


def match_schema_errors(exception, expected):
    assert_unordered_lists(
        [
            message.split(":", maxsplit=1)[1].strip()
            for message in str(exception).strip().splitlines()
        ],
        expected,
    )
