from unittest.mock import MagicMock


class AsyncMock(MagicMock):
    """Fix to be able to use MagicMock with async context"""

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
