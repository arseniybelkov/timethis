from timethis import timethis


def mocked_logger_function(pattern: str):
    def _logger(log_entry: str):
        assert pattern in log_entry
        return log_entry

    return _logger


def test_function():
    # Setting up log_callback is optional (defaults to `print`),
    # here it is merely done for the testing.
    @timethis(log_callback=mocked_logger_function("some_func"))
    def some_func():
        import time
        time.sleep(0.1)


def test_function_custom_name():
    @timethis("some_other_name", log_callback=mocked_logger_function("some_other_name"))
    def some_other_func():
        import time
        time.sleep(0.1)


def test_lambda():
    from collections import Counter

    result = timethis("some code scope", log_callback=mocked_logger_function("some code scope"))(
        lambda: Counter([1, 1, 3]).most_common(1)[0]
    )()
    assert result[0] == 1